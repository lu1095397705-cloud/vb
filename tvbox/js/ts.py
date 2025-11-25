import requests
import json
import re
from urllib.parse import quote, unquote, urljoin
from bs4 import BeautifulSoup
import time
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MiqkSource:
    def __init__(self):
        self.name = "至臻影视"
        self.host = "https://www.miqk.cc"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': self.host
        }
        self.timeout = 15
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def homeContent(self, filter):
        """首页分类"""
        result = {}
        try:
            # 根据测试结果，网站有这些分类
            classes = [
                {"type_id": "26", "type_name": "臻彩严选"},
                {"type_id": "1", "type_name": "至臻电影"},
                {"type_id": "2", "type_name": "至臻剧集"},
                {"type_id": "3", "type_name": "至臻动漫"},
                {"type_id": "5", "type_name": "短剧吃到饱"},
                {"type_id": "24", "type_name": "老剧计划"},
                {"type_id": "25", "type_name": "纪录片"}
            ]
            result['class'] = classes
            logger.info("首页分类加载成功")
        except Exception as e:
            logger.error(f"首页分类获取失败: {e}")
            result['class'] = []

        return result

    def homeVideoContent(self):
        """首页推荐视频"""
        result = {'list': []}
        try:
            # 获取首页内容
            response = self.session.get(self.host, timeout=self.timeout)
            if response.status_code != 200:
                logger.error(f"首页请求失败: {response.status_code}")
                return result

            soup = BeautifulSoup(response.text, 'html.parser')
            videos = self.parse_home_videos(soup)
            result['list'] = videos
            logger.info(f"首页获取到 {len(videos)} 个推荐视频")

        except Exception as e:
            logger.error(f"首页视频获取失败: {e}")

        return result

    def parse_home_videos(self, soup):
        """解析首页视频"""
        videos = []
        try:
            # 尝试多种可能的选择器
            selectors = [
                '.module-item',
                '.vod-item',
                '.video-item',
                '.item',
                'li'
            ]

            for selector in selectors:
                items = soup.select(selector)
                if items and len(items) > 5:  # 至少有5个才认为是正确的选择器
                    logger.info(f"使用选择器 '{selector}' 找到 {len(items)} 个项目")
                    for item in items[:20]:  # 只处理前20个
                        video = self.parse_video_item(item)
                        if video:
                            videos.append(video)
                    break

            # 如果没有找到，尝试更通用的方法
            if not videos:
                videos = self.fallback_parse(soup)

        except Exception as e:
            logger.error(f"解析首页视频失败: {e}")

        return videos

    def parse_video_item(self, item):
        """解析单个视频项"""
        try:
            video = {}

            # 查找链接
            link = item.find('a', href=True)
            if not link:
                return None

            href = link.get('href', '')
            if not href or 'vod/detail' not in href:
                return None

            video['vod_id'] = href

            # 查找标题
            title_selectors = [
                link.get('title'),
                link.get_text(strip=True),
                item.find('img', alt=True) and item.find('img').get('alt'),
                item.find('h3') and item.find('h3').get_text(strip=True),
                item.find('h4') and item.find('h4').get_text(strip=True)
            ]

            for title in title_selectors:
                if title and len(title) > 1:
                    video['vod_name'] = title
                    break
            else:
                video['vod_name'] = '未知标题'

            # 查找图片
            img = item.find('img')
            if img:
                img_src = img.get('data-src') or img.get('src')
                if img_src:
                    video['vod_pic'] = self.complete_url(img_src)

            # 查找备注信息
            remark_selectors = ['.remarks', '.tag', '.score', '.year']
            for selector in remark_selectors:
                elem = item.select_one(selector)
                if elem:
                    video['vod_remarks'] = elem.get_text(strip=True)
                    break

            return video

        except Exception as e:
            logger.warning(f"解析视频项失败: {e}")
            return None

    def fallback_parse(self, soup):
        """备用解析方法"""
        videos = []
        try:
            # 查找所有包含vod/detail的链接
            detail_links = soup.find_all('a', href=re.compile(r'vod/detail'))
            logger.info(f"找到 {len(detail_links)} 个详情链接")

            for link in detail_links[:20]:
                try:
                    href = link.get('href')
                    title = link.get('title') or link.get_text(strip=True)

                    if href and title and len(title) > 1:
                        video = {
                            'vod_id': href,
                            'vod_name': title,
                            'vod_pic': '',
                            'vod_remarks': '影视'
                        }
                        videos.append(video)
                except:
                    continue

        except Exception as e:
            logger.error(f"备用解析失败: {e}")

        return videos

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容"""
        result = {}
        videos = []

        try:
            # 构建分类URL - 使用测试中发现的正确格式
            if int(pg) == 1:
                url = f"{self.host}/index.php/vod/type/id/{tid}.html"
            else:
                url = f"{self.host}/index.php/vod/type/id/{tid}/page/{pg}.html"

            logger.info(f"分类URL: {url}")

            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logger.error(f"分类页面请求失败: {response.status_code}")
                result['list'] = []
                return result

            soup = BeautifulSoup(response.text, 'html.parser')
            videos = self.parse_category_videos(soup)

        except Exception as e:
            logger.error(f"分类内容获取失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999 if videos else 1
        result['limit'] = len(videos)
        result['total'] = len(videos) * 20

        logger.info(f"分类 {tid} 第 {pg} 页获取到 {len(videos)} 个视频")
        return result

    def parse_category_videos(self, soup):
        """解析分类页面视频"""
        videos = []
        try:
            # 与方法1相同，查找视频项
            items = soup.find_all('a', href=re.compile(r'vod/detail'))
            for item in items:
                video = self.parse_video_item(item.parent) if item.parent else self.parse_video_item(item)
                if video:
                    videos.append(video)

            # 去重
            seen = set()
            unique_videos = []
            for v in videos:
                if v['vod_id'] not in seen:
                    seen.add(v['vod_id'])
                    unique_videos.append(v)

            return unique_videos

        except Exception as e:
            logger.error(f"解析分类视频失败: {e}")
            return []

    def detailContent(self, ids):
        """详情内容"""
        result = {}
        vod_id = ids[0]

        try:
            # 确保vod_id是完整URL
            if not vod_id.startswith('http'):
                url = f"{self.host}{vod_id}" if vod_id.startswith('/') else f"{self.host}/{vod_id}"
            else:
                url = vod_id

            logger.info(f"详情URL: {url}")

            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logger.error(f"详情页面请求失败: {response.status_code}")
                result['list'] = []
                return result

            soup = BeautifulSoup(response.text, 'html.parser')
            vod_detail = self.parse_detail(soup, vod_id)
            result['list'] = [vod_detail] if vod_detail else []

        except Exception as e:
            logger.error(f"详情内容获取失败: {e}")
            result['list'] = []

        return result

    def parse_detail(self, soup, vod_id):
        """解析详情页面"""
        try:
            vod_detail = {}
            vod_detail['vod_id'] = vod_id

            # 标题
            title = soup.find('title')
            if title:
                vod_detail['vod_name'] = title.get_text(strip=True)

            # 封面图片
            img = soup.find('img', src=re.compile(r'\.(jpg|jpeg|png|webp)'))
            if img:
                img_src = img.get('data-src') or img.get('src')
                if img_src:
                    vod_detail['vod_pic'] = self.complete_url(img_src)

            # 剧情简介
            content_selectors = ['.content', '.intro', '.description', '.summary']
            for selector in content_selectors:
                elem = soup.select_one(selector)
                if elem:
                    vod_detail['vod_content'] = elem.get_text(strip=True)
                    break

            # 播放链接
            play_from, play_url = self.extract_play_links(soup)
            if play_from and play_url:
                vod_detail['vod_play_from'] = '$$$'.join(play_from)
                vod_detail['vod_play_url'] = '$$$'.join(play_url)

            return vod_detail

        except Exception as e:
            logger.error(f"解析详情失败: {e}")
            return None

    def extract_play_links(self, soup):
        """提取播放链接"""
        play_from = []
        play_url = []

        try:
            # 查找所有可能的播放链接
            links = []

            # 网盘链接
            pan_patterns = [
                r'https?://pan\.baidu\.com/s/[\w-]+',
                r'https?://www\.aliyundrive\.com/s/[\w]+',
                r'https?://cloud\.189\.cn/.+',
                r'https?://[^\s<>"\']+\.(m3u8|mp4|avi|mkv)'
            ]

            text = soup.get_text()
            for pattern in pan_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                links.extend(matches)

            # 去重
            links = list(set(links))

            if links:
                play_from.append('播放线路')
                url_parts = []

                for i, link in enumerate(links, 1):
                    url_parts.append(f"第{i}集${link}")

                play_url.append('#'.join(url_parts))
                logger.info(f"找到 {len(links)} 个播放链接")

        except Exception as e:
            logger.error(f"提取播放链接失败: {e}")

        return play_from, play_url

    def searchContent(self, key, quick, pg):
        """搜索内容"""
        result = {}
        videos = []

        try:
            encoded_key = quote(key)
            url = f"{self.host}/index.php/vod/search/page/{pg}/wd/{encoded_key}.html"
            logger.info(f"搜索URL: {url}")

            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logger.error(f"搜索请求失败: {response.status_code}")
                result['list'] = []
                return result

            soup = BeautifulSoup(response.text, 'html.parser')
            videos = self.parse_category_videos(soup)  # 搜索页面结构与分类页面类似

        except Exception as e:
            logger.error(f"搜索失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999 if videos else 1
        result['limit'] = len(videos)
        result['total'] = len(videos) * 20

        logger.info(f"搜索 '{key}' 获得 {len(videos)} 个结果")
        return result

    def playerContent(self, flag, id, flags):
        """播放器内容"""
        result = {}

        try:
            result["parse"] = 0  # 不解析，直接播放
            result["playUrl"] = ""
            result["url"] = id
            result["header"] = json.dumps(self.headers)

        except Exception as e:
            logger.error(f"播放器内容失败: {e}")

        return result

    def complete_url(self, url):
        """补全URL"""
        if not url:
            return ''
        if url.startswith('http'):
            return url
        if url.startswith('//'):
            return 'https:' + url
        if url.startswith('/'):
            return self.host + url
        return self.host + '/' + url

    def localProxy(self, param):
        """本地代理"""
        return {}


# 创建实例
source = MiqkSource()


# TVBox标准接口
def homeContent(filter):
    return source.homeContent(filter)


def homeVideoContent():
    return source.homeVideoContent()


def categoryContent(tid, pg, filter, extend):
    return source.categoryContent(tid, pg, filter, extend)


def detailContent(ids):
    return source.detailContent(ids)


def searchContent(key, quick, pg):
    return source.searchContent(key, quick, pg)


def playerContent(flag, id, flags):
    return source.playerContent(flag, id, flags)


def localProxy(param):
    return source.localProxy(param)