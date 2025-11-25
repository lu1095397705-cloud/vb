import requests
from bs4 import BeautifulSoup
import json
import re


class ZhiZhenSource:
    def __init__(self):
        self.webSite = 'http://www.miqk.cc'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def homeContent(self, filter):
        result = {}
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
        return result

    def homeVideoContent(self):
        # 首页推荐视频，这里可以留空或实现推荐功能
        return []

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        videos = []

        try:
            url = f"{self.webSite.rstrip('/')}/index.php/vod/show/id/{tid}/page/{pg}.html"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            vod_items = soup.select('#main .module-item')
            for item in vod_items:
                video = {}

                # 获取视频链接
                link_tag = item.select_one('.module-item-pic a')
                if link_tag and link_tag.get('href'):
                    video['vod_id'] = link_tag['href']

                # 获取视频名称
                img_tag = item.select_one('.module-item-pic img')
                if img_tag and img_tag.get('alt'):
                    video['vod_name'] = img_tag['alt']

                # 获取封面图片
                if img_tag and img_tag.get('data-src'):
                    video['vod_pic'] = self.combine_url(img_tag['data-src'])

                # 获取备注信息
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
            print(f"获取分类内容失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999  # 假设有足够多的页数
        result['limit'] = len(videos)
        result['total'] = len(videos) * 10  # 估算总数

        return result

    def detailContent(self, array):
        tid = array[0]
        result = {}

        try:
            url = f"{self.webSite.rstrip('/')}{tid}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            vod_detail = {}
            vod_detail['vod_id'] = tid

            # 获取标题
            title_tag = soup.select_one('.page-title')
            if title_tag:
                vod_detail['vod_name'] = title_tag.get_text().strip()

            # 获取封面
            pic_tag = soup.select_one('.mobile-play .lazyload')
            if pic_tag and pic_tag.get('data-src'):
                vod_detail['vod_pic'] = self.combine_url(pic_tag['data-src'])

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

            # 解析播放链接
            play_from = []
            play_url = []
            pan_urls = []

            # 获取网盘链接
            pan_items = soup.select('.module-row-info')
            for item in pan_items:
                p_tag = item.find('p')
                if p_tag:
                    share_url = p_tag.get_text().strip()
                    if share_url:
                        pan_urls.append(share_url)

            # 将网盘链接组织成播放列表
            if pan_urls:
                play_from.append('至臻网盘')
                play_urls = []
                for i, pan_url in enumerate(pan_urls, 1):
                    play_urls.append(f"第{i集}${pan_url}")
                play_url.append('#'.join(play_urls))

            if play_from and play_url:
                vod_detail['vod_play_from'] = '$$$'.join(play_from)
                vod_detail['vod_play_url'] = '$$$'.join(play_url)

            result['list'] = [vod_detail]

        except Exception as e:
            print(f"获取详情失败: {e}")
            result['list'] = []

        return result

    def searchContent(self, key, quick, pg):
        result = {}
        videos = []

        try:
            url = f"{self.webSite.rstrip('/')}/index.php/vod/search/page/{pg}/wd/{key}.html"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.select('.module-search-item')
            for item in items:
                video = {}

                # 获取视频链接
                link_tag = item.select_one('.video-serial')
                if link_tag and link_tag.get('href'):
                    video['vod_id'] = link_tag['href']

                # 获取视频名称
                if link_tag and link_tag.get('title'):
                    video['vod_name'] = link_tag['title']

                # 获取封面
                img_tag = item.select_one('.module-item-pic > img')
                if img_tag and img_tag.get('data-src'):
                    video['vod_pic'] = self.combine_url(img_tag['data-src'])

                # 获取备注
                if link_tag:
                    video['vod_remarks'] = link_tag.get_text().strip()

                if video.get('vod_id') and video.get('vod_name'):
                    videos.append(video)

        except Exception as e:
            print(f"搜索失败: {e}")

        result['list'] = videos
        result['page'] = int(pg)
        result['pagecount'] = 999
        result['limit'] = len(videos)
        result['total'] = len(videos) * 10

        return result

    def playerContent(self, flag, id, flags):
        result = {}

        # 这里直接返回网盘链接，TVBox会调用相应的解析器
        result["parse"] = 0  # 不解析，直接播放
        result["playUrl"] = ""
        result["url"] = id
        result["header"] = json.dumps(self.headers)

        return result

    def combine_url(self, url):
        if not url:
            return ''
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return self.webSite + url
        return self.webSite + '/' + url

    def isVideoFormat(self, url):
        # 判断是否为视频格式
        video_formats = ['.m3u8', '.mp4', '.flv', '.avi', '.mkv', '.mov', '.wmv', '.webm']
        return any(url.lower().endswith(fmt) for fmt in video_formats)

    def localProxy(self, param):
        # 本地代理，如果需要的话
        return []


# 创建实例
source = ZhiZhenSource()


# TVBox标准接口函数
def homeContent(filter):
    return source.homeContent(filter)


def homeVideoContent():
    return source.homeVideoContent()


def categoryContent(tid, pg, filter, extend):
    return source.categoryContent(tid, pg, filter, extend)


def detailContent(array):
    return source.detailContent(array)


def searchContent(key, quick, pg):
    return source.searchContent(key, quick, pg)


def playerContent(flag, id, flags):
    return source.playerContent(flag, id, flags)


def localProxy(param):
    return source.localProxy(param)