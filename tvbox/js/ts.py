import requests
import json
import re
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ZhiZhenSource:
    def __init__(self):
        self.name = "至臻"
        self.host = "http://www.miqk.cc"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.host,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.timeout = 15
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def make_request(self, url, max_retries=3):
        """带重试的请求函数"""
        for i in range(max_retries):
            try:
                logger.info(f"请求URL: {url}")
                response = self.session.get(url, timeout=self.timeout)
                response.encoding = 'utf-8'

                # 检查响应状态
                if response.status_code != 200:
                    logger.warning(f"请求失败，状态码: {response.status_code}")
                    continue

                # 检查响应内容是否有效
                if not response.text or len(response.text) < 100:
                    logger.warning("响应内容过短或为空")
                    continue

                logger.info(f"请求成功，内容长度: {len(response.text)}")
                return response

            except Exception as e:
                logger.error(f"第{i + 1}次请求失败: {str(e)}")
                if i < max_retries - 1:
                    time.sleep(2)  # 重试前等待
                continue

        return None

    def homeContent(self, filter):
        """首页分类"""
        result = {}
        try:
            classes = [
                {"type_id": "1", "type_name": "至臻电影"},
                {"type_id": "2", "type_name": "至臻剧集"},
                {"type_id": "3", "type_name": "至臻动漫"},
                {"type_id": "4", "type_name": "至臻综艺"},
                {"type_id": "5", "type_name": "至臻短剧"},
                {"type_id": "24", "type_name": "至臻老剧"},
                {"type_id": "26", "type_name": "至臻严选"}
            ]
            result['class'] = classes
            logger.info(f"加载分类成功: {len(classes)}个分类")
        except Exception as e:
            logger.error(f"首页分类获取失败: {e}")
            result['class'] = []

        return result

    def homeVideoContent(self):
        """首页推荐视频"""
        result = {'list': []}
        try:
            # 尝试获取首页推荐内容
            response = self.make_request(self.host)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 多种选择器尝试
                selectors = [
                    '.module-item',
                    '.vod-item',
                    '.video-item',
                    '[class*="item"]',
                    '.list-item'
                ]

                for selector in selectors:
                    items = soup.select(selector)
                    if items:
                        logger.info(f"使用选择器 '{selector}' 找到 {len(items)} 个项目")
                        for item in items[:10]:  # 只取前10个
                            try:
                                video = self.parse_video_item(item)
                                if video:
                                    result['list'].append(video)
                            except Exception as e:
                                logger.warning(f"解析视频项失败: {e}")
                        break

                if not result['list']:
                    logger.warning("未找到视频内容，尝试调试页面结构")
                    self.debug_page_structure(soup)

        except Exception as e:
            logger.error(f"首页视频获取失败: {e}")

        # 如果没有数据，返回示例数据用于测试
        if not result['list']:
            result['list'] = [{
                'vod_id': '/vod/detail/id/1.html',
                'vod_name': '测试视频',
                'vod_pic': 'https://example.com/pic.jpg',
                'vod_remarks': '测试'
            }]

        return result

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容"""
        result = {}
        videos = []

        try:
            url = f"{self.host.rstrip('/')}/vod/show/id/{tid}/page/{pg}.html"
            logger.info(f"分类页面URL: {url}")

            response = self.make_request(url)
            if not response:
                logger.error("无法获取分类页面")
                result['list'] = []
                result['page'] = int(pg)
                result['pagecount'] = 1
                result['limit'] = 0
                result['total'] = 0
                return result

            soup = BeautifulSoup(response.text, 'html.parser')

            # 调试：保存页面内容用于分析
            with open(f"debug_page_{tid}_{pg}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            logger.info(f"页面已保存为 debug_page_{tid}_{pg}.html")

            # 多种视频项选择器尝试
            video_selectors = [
                '.module-item',
                '.vod-item',
                '.video-item',
                '.item',
                '[class*="item"]',
                'li',
                '.list-item'
            ]

            for selector in video_selectors:
                vod_items = soup.select(selector)
                if vod_items and len(vod_items) > 2:  # 至少有3个项目才认为是有效的
                    logger.info(f"使用选择器 '{selector}' 找到 {len(vod_items)} 个视频项")

                    for item in vod_items:
                        try:
                            video = self.parse_video_item(item)
                            if video:
                                videos.append(video)
                        except Exception as e:
                            logger.warning(f"解析视频项失败: {e}")
                    break

            if not videos:
                logger.warning("未找到视频内容，分析页面结构...")
                self.debug_page_structure(soup)

        except Exception as e:
            logger.error(f"分类内容获取失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999 if videos else 1
        result['limit'] = len(videos)
        result['total'] = len(videos) * 10

        logger.info(f"分类 {tid} 第 {pg} 页获取到 {len(videos)} 个视频")
        return result

    def parse_video_item(self, item):
        """解析单个视频项"""
        try:
            video = {}

            # 尝试多种链接选择器
            link_selectors = ['a', '.pic a', 'h3 a', '.title a', '[href*="vod"]']
            for selector in link_selectors:
                link_tag = item.select_one(selector)
                if link_tag and link_tag.get('href'):
                    href = link_tag['href']
                    if href and not href.startswith('javascript'):
                        video['vod_id'] = href
                        break

            # 尝试多种标题选择器
            title_selectors = ['img[alt]', '.title', 'h3', 'h4', '[title]']
            for selector in title_selectors:
                title_tag = item.select_one(selector)
                if title_tag:
                    title = title_tag.get('alt') or title_tag.get('title') or title_tag.get_text().strip()
                    if title and len(title) > 1:
                        video['vod_name'] = title
                        break

            # 尝试多种图片选择器
            img_selectors = ['img', '.pic img', '.lazyload', '[data-src]', '[src]']
            for selector in img_selectors:
                img_tag = item.select_one(selector)
                if img_tag:
                    img_src = img_tag.get('data-src') or img_tag.get('src')
                    if img_src:
                        video['vod_pic'] = self.complete_url(img_src)
                        break

            # 尝试多种备注选择器
            remark_selectors = ['.remark', '.text', '.subtitle', '.tag', '.score']
            for selector in remark_selectors:
                remark_tag = item.select_one(selector)
                if remark_tag:
                    remark = remark_tag.get_text().strip()
                    if remark:
                        video['vod_remarks'] = remark
                        break

            # 验证必要字段
            if not video.get('vod_id') or not video.get('vod_name'):
                return None

            return video

        except Exception as e:
            logger.warning(f"解析视频项失败: {e}")
            return None

    def debug_page_structure(self, soup):
        """调试页面结构"""
        logger.info("=== 页面结构分析 ===")

        # 分析所有链接
        links = soup.find_all('a', href=True)
        logger.info(f"页面中共有 {len(links)} 个链接")

        # 分析视频相关链接
        vod_links = [a for a in links if 'vod' in a['href']]
        logger.info(f"视频相关链接: {len(vod_links)} 个")
        for link in vod_links[:5]:  # 显示前5个
            logger.info(f"链接: {link['href']}, 文本: {link.get_text().strip()[:50]}")

        # 分析图片
        imgs = soup.find_all('img', src=True)
        logger.info(f"页面中共有 {len(imgs)} 个图片")

        # 分析类名模式
        all_classes = set()
        for tag in soup.find_all(class_=True):
            all_classes.update(tag.get('class', []))

        logger.info(f"页面中使用的CSS类: {list(all_classes)[:20]}")  # 显示前20个

        logger.info("=== 分析结束 ===")

    def detailContent(self, ids):
        """详情内容"""
        result = {}
        vod_id = ids[0]

        try:
            # 确保vod_id以/开头
            if not vod_id.startswith('/'):
                vod_id = '/' + vod_id.lstrip('/')

            url = f"{self.host.rstrip('/')}{vod_id}"
            logger.info(f"详情页面URL: {url}")

            response = self.make_request(url)
            if not response:
                logger.error("无法获取详情页面")
                result['list'] = []
                return result

            soup = BeautifulSoup(response.text, 'html.parser')

            # 保存详情页面用于调试
            with open("debug_detail.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            logger.info("详情页面已保存为 debug_detail.html")

            vod_detail = {}
            vod_detail['vod_id'] = vod_id

            # 标题选择器
            title_selectors = ['.page-title', 'h1', 'title', '.title', 'header h1']
            for selector in title_selectors:
                title_tag = soup.select_one(selector)
                if title_tag:
                    title = title_tag.get_text().strip()
                    if title:
                        vod_detail['vod_name'] = title
                        break

            # 图片选择器
            img_selectors = ['.lazyload', 'img[data-src]', '.poster img', '.cover img', 'img']
            for selector in img_selectors:
                img_tag = soup.select_one(selector)
                if img_tag:
                    img_src = img_tag.get('data-src') or img_tag.get('src')
                    if img_src:
                        vod_detail['vod_pic'] = self.complete_url(img_src)
                        break

            # 内容选择器
            content_selectors = ['.content', '.description', '.intro', '.summary']
            for selector in content_selectors:
                content_tag = soup.select_one(selector)
                if content_tag:
                    content = content_tag.get_text().strip()
                    if content:
                        vod_detail['vod_content'] = content
                        break

            # 播放链接提取
            play_from, play_url = self.extract_play_urls(soup)
            if play_from and play_url:
                vod_detail['vod_play_from'] = '$$$'.join(play_from)
                vod_detail['vod_play_url'] = '$$$'.join(play_url)

            result['list'] = [vod_detail]
            logger.info(f"详情解析完成: {vod_detail.get('vod_name', '未知')}")

        except Exception as e:
            logger.error(f"详情内容获取失败: {e}")
            result['list'] = []

        return result

    def extract_play_urls(self, soup):
        """提取播放链接"""
        play_from = []
        play_url = []

        try:
            # 多种播放链接选择器
            url_patterns = [
                r'https?://[^\s<>"\'{}|\\^`]+\.(m3u8|mp4|flv|avi|mkv|mov|wmv|webm)',
                r'https?://pan\.baidu\.com/s/[^\s<>"\']+',
                r'https?://www\.aliyundrive\.com/s/[^\s<>"\']+',
                r'https?://cloud\.189\.cn/[^\s<>"\']+'
            ]

            # 在页面文本中搜索
            page_text = soup.get_text()
            all_urls = []

            for pattern in url_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                all_urls.extend(matches)

            # 去重
            all_urls = list(set(all_urls))

            if all_urls:
                play_from.append('播放线路')
                url_parts = []

                for i, url in enumerate(all_urls, 1):
                    pan_name = self.get_pan_name(url)
                    url_parts.append(f"第{i}集${url}")

                play_url.append('#'.join(url_parts))
                logger.info(f"找到 {len(all_urls)} 个播放链接")

        except Exception as e:
            logger.error(f"提取播放链接失败: {e}")

        return play_from, play_url

    def searchContent(self, key, quick, pg):
        """搜索内容"""
        result = {}
        videos = []

        try:
            encoded_key = quote(key)
            url = f"{self.host.rstrip('/')}/index.php/vod/search/page/{pg}/wd/{encoded_key}.html"
            logger.info(f"搜索URL: {url}")

            response = self.make_request(url)
            if not response:
                logger.error("搜索请求失败")
                result['list'] = []
                result['page'] = int(pg)
                result['pagecount'] = 1
                result['limit'] = 0
                result['total'] = 0
                return result

            soup = BeautifulSoup(response.text, 'html.parser')

            # 多种搜索结果选择器
            selectors = ['.module-search-item', '.search-item', '.result-item', '.item']

            for selector in selectors:
                items = soup.select(selector)
                if items:
                    logger.info(f"搜索找到 {len(items)} 个结果")
                    for item in items:
                        video = self.parse_video_item(item)
                        if video:
                            videos.append(video)
                    break

            if not videos:
                logger.warning("搜索未找到结果")

        except Exception as e:
            logger.error(f"搜索失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999 if videos else 1
        result['limit'] = len(videos)
        result['total'] = len(videos) * 10

        logger.info(f"搜索 '{key}' 获得 {len(videos)} 个结果")
        return result

    def playerContent(self, flag, id, flags):
        """播放器内容"""
        result = {}

        try:
            result["parse"] = 0
            result["playUrl"] = ""
            result["url"] = id
            result["header"] = json.dumps(self.headers)
            logger.info(f"播放请求: {id}")

        except Exception as e:
            logger.error(f"播放器内容获取失败: {e}")

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

    def get_pan_name(self, url):
        """获取网盘名称"""
        if 'baidu' in url:
            return '百度网盘'
        elif 'aliyundrive' in url:
            return '阿里云盘'
        elif '189.cn' in url:
            return '天翼云盘'
        elif any(ext in url for ext in ['.m3u8', '.mp4', '.flv']):
            return '直连'
        else:
            return '网盘'

    def localProxy(self, param):
        """本地代理"""
        return {}


# 创建全局实例
source = ZhiZhenSource()


# TVBox标准接口函数
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