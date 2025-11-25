import requests
import json
import re
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
import time


class ZhiZhenSource:
    def __init__(self):
        self.name = "至臻"
        self.host = "http://www.miqk.cc"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.host
        }
        self.timeout = 10

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
        except Exception as e:
            print(f"首页分类获取失败: {e}")
            result['class'] = []

        return result

    def homeVideoContent(self):
        """首页推荐视频"""
        result = {'list': []}
        try:
            # 可以在这里添加首页推荐视频逻辑
            pass
        except Exception as e:
            print(f"首页视频获取失败: {e}")

        return result

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容"""
        result = {}
        videos = []

        try:
            url = f"{self.host.rstrip('/')}/index.php/vod/show/id/{tid}/page/{pg}.html"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            vod_items = soup.select('#main .module-item')

            for item in vod_items:
                try:
                    video = {}

                    # 获取链接
                    link_tag = item.select_one('.module-item-pic a')
                    if link_tag and link_tag.get('href'):
                        video['vod_id'] = link_tag['href']

                    # 获取标题
                    img_tag = item.select_one('.module-item-pic img')
                    if img_tag and img_tag.get('alt'):
                        video['vod_name'] = img_tag['alt']

                    # 获取图片
                    if img_tag and img_tag.get('data-src'):
                        video['vod_pic'] = self.complete_url(img_tag['data-src'])

                    # 获取备注
                    remark_tag = item.select_one('.module-item-text')
                    if remark_tag:
                        video['vod_remarks'] = remark_tag.get_text().strip()

                    # 获取年份
                    year_tag = item.select_one('.module-item-caption span')
                    if year_tag:
                        video['vod_year'] = year_tag.get_text().strip()

                    if video.get('vod_id') and video.get('vod_name'):
                        videos.append(video)

                except Exception as e:
                    print(f"解析视频项失败: {e}")
                    continue

        except Exception as e:
            print(f"分类内容获取失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999
        result['limit'] = len(videos)
        result['total'] = len(videos) * 10

        return result

    def detailContent(self, ids):
        """详情内容"""
        result = {}
        vod_id = ids[0]

        try:
            url = f"{self.host.rstrip('/')}{vod_id}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            vod_detail = {}
            vod_detail['vod_id'] = vod_id

            # 获取标题
            title_tag = soup.select_one('.page-title')
            if title_tag:
                vod_detail['vod_name'] = title_tag.get_text().strip()

            # 获取封面
            pic_tag = soup.select_one('.mobile-play .lazyload')
            if pic_tag and pic_tag.get('data-src'):
                vod_detail['vod_pic'] = self.complete_url(pic_tag['data-src'])

            # 解析视频信息
            info_items = soup.select('.video-info-itemtitle')

            for item in info_items:
                key = item.get_text().strip()
                next_sibling = item.find_next_sibling()

                if not next_sibling:
                    continue

                if '剧情' in key:
                    content_tag = next_sibling.find('p')
                    if content_tag:
                        vod_detail['vod_content'] = content_tag.get_text().strip()
                elif '导演' in key:
                    directors = []
                    director_tags = next_sibling.find_all('a')
                    for tag in director_tags:
                        text = tag.get_text().strip()
                        if text:
                            directors.append(text)
                    if directors:
                        vod_detail['vod_director'] = ','.join(directors)
                elif '主演' in key:
                    actors = []
                    actor_tags = next_sibling.find_all('a')
                    for tag in actor_tags:
                        text = tag.get_text().strip()
                        if text:
                            actors.append(text)
                    if actors:
                        vod_detail['vod_actor'] = ','.join(actors)

            # 解析网盘链接
            pan_urls = []
            pan_items = soup.select('.module-row-info')

            for item in pan_items:
                p_tag = item.find('p')
                if p_tag:
                    share_url = p_tag.get_text().strip()
                    if share_url and self.is_valid_url(share_url):
                        pan_urls.append(share_url)

            # 组织播放列表
            play_from = []
            play_url = []

            if pan_urls:
                # 创建一个播放线路
                play_from.append('至臻网盘')
                url_parts = []

                for i, pan_url in enumerate(pan_urls, 1):
                    # 提取网盘名称
                    pan_name = self.get_pan_name(pan_url)
                    url_parts.append(f"第{i}集[{pan_name}]${pan_url}")

                play_url.append('#'.join(url_parts))

            if play_from and play_url:
                vod_detail['vod_play_from'] = '$$$'.join(play_from)
                vod_detail['vod_play_url'] = '$$$'.join(play_url)

            result['list'] = [vod_detail]

        except Exception as e:
            print(f"详情内容获取失败: {e}")
            result['list'] = []

        return result

    def searchContent(self, key, quick, pg):
        """搜索内容"""
        result = {}
        videos = []

        try:
            encoded_key = quote(key)
            url = f"{self.host.rstrip('/')}/index.php/vod/search/page/{pg}/wd/{encoded_key}.html"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.module-search-item')

            for item in items:
                try:
                    video = {}

                    # 获取链接
                    link_tag = item.select_one('.video-serial')
                    if link_tag and link_tag.get('href'):
                        video['vod_id'] = link_tag['href']

                    # 获取标题
                    if link_tag and link_tag.get('title'):
                        video['vod_name'] = link_tag['title']

                    # 获取图片
                    img_tag = item.select_one('.module-item-pic > img')
                    if img_tag and img_tag.get('data-src'):
                        video['vod_pic'] = self.complete_url(img_tag['data-src'])

                    # 获取备注
                    if link_tag:
                        video['vod_remarks'] = link_tag.get_text().strip()

                    if video.get('vod_id') and video.get('vod_name'):
                        videos.append(video)

                except Exception as e:
                    print(f"解析搜索结果失败: {e}")
                    continue

        except Exception as e:
            print(f"搜索失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999
        result['limit'] = len(videos)
        result['total'] = len(videos) * 10

        return result

    def playerContent(self, flag, id, flags):
        """播放器内容"""
        result = {}

        try:
            # 对于网盘链接，直接返回原始URL
            result["parse"] = 0  # 0=不解析，1=解析
            result["playUrl"] = ""
            result["url"] = id
            result["header"] = json.dumps(self.headers)

        except Exception as e:
            print(f"播放器内容获取失败: {e}")

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

    def is_valid_url(self, url):
        """检查是否为有效URL"""
        if not url:
            return False
        url_patterns = [
            r'https?://pan\.baidu\.com',
            r'https?://www\.aliyundrive\.com',
            r'https?://cloud\.189\.cn',
            r'https?://.*\.m3u8',
            r'https?://.*\.mp4',
            r'https?://.*\.avi',
            r'https?://.*\.mkv'
        ]
        return any(re.search(pattern, url, re.I) for pattern in url_patterns)

    def get_pan_name(self, url):
        """获取网盘名称"""
        if 'baidu' in url:
            return '百度'
        elif 'aliyundrive' in url:
            return '阿里'
        elif '189.cn' in url:
            return '天翼'
        elif 'm3u8' in url:
            return '直链'
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