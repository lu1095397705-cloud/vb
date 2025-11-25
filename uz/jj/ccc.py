import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from typing import List, Dict, Any, Optional
import re


class VideoCrawler:
    """视频爬虫类 - 至臻视频网站爬取"""

    def __init__(self, base_url: str = "http://www.miqk.cc"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # 设置请求头，模拟浏览器访问
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get_class_list(self) -> str:
        """
        获取分类列表
        对应原JS的getClassList函数
        返回JSON字符串
        """
        # 创建分类列表
        categories = [
            {
                'type_id': '1',
                'type_name': '至臻电影',
                'hasSubclass': False,
            },
            {
                'type_id': '2',
                'type_name': '至臻剧集',
                'hasSubclass': False,
            },
            {
                'type_id': '3',
                'type_name': '至臻动漫',
                'hasSubclass': False,
            },
            {
                'type_id': '4',
                'type_name': '至臻综艺',
                'hasSubclass': False,
            },
            {
                'type_id': '5',
                'type_name': '至臻短剧',
                'hasSubclass': False,
            },
            {
                'type_id': '24',
                'type_name': '至臻老剧',
                'hasSubclass': False,
            },
            {
                'type_id': '26',
                'type_name': '至臻严选',
                'hasSubclass': False,
            },
        ]

        # 创建响应对象
        back_data = {
            'data': categories,
            'error': None
        }

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)

    def get_subclass_list(self, args: Dict[str, Any]) -> str:
        """
        获取子分类列表
        对应原JS的getSubclassList函数
        返回JSON字符串
        """
        # 创建空响应对象
        back_data = {
            'data': [],
            'error': None
        }

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)

    def get_subclass_video_list(self, args: Dict[str, Any]) -> str:
        """
        获取子分类视频列表
        对应原JS的getSubclassVideoList函数
        返回JSON字符串
        """
        # 创建空响应对象
        back_data = {
            'data': [],
            'error': None
        }

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)

    def get_video_list(self, args: Dict[str, Any]) -> str:
        """
        获取分类视频列表
        对应原JS的getVideoList函数

        Args:
            args: 包含url和page参数的字典
        """
        # 提取参数
        category_id = args.get('url', '')
        page = args.get('page', 1)

        # 构建URL
        url = f"{self.base_url}/index.php/vod/show/id/{category_id}/page/{page}.html"

        # 创建响应对象
        back_data = {
            'data': [],
            'error': None
        }

        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                back_data['error'] = f"请求失败，状态码: {response.status_code}"
                return json.dumps(back_data, ensure_ascii=False)

            soup = BeautifulSoup(response.text, 'html.parser')
            videos = []

            # 查找视频项
            vod_items = soup.select('.module-item')

            for item in vod_items:
                video_info = {}

                # 提取视频链接
                link_element = item.select_one('.module-item-pic a')
                if link_element and link_element.get('href'):
                    video_info['vod_id'] = link_element['href']

                # 提取视频名称
                img_element = item.select_one('.module-item-pic img')
                if img_element:
                    video_info['vod_name'] = img_element.get('alt', '').strip()
                    video_info['vod_pic'] = img_element.get('data-src', '')

                # 提取备注信息
                remark_element = item.select_one('.module-item-text')
                if remark_element:
                    video_info['vod_remarks'] = remark_element.get_text(strip=True)

                # 提取年份信息
                year_element = item.select_one('.module-item-caption span')
                if year_element:
                    video_info['vod_year'] = year_element.get_text(strip=True)

                if video_info:  # 确保有数据才添加
                    videos.append(video_info)

            back_data['data'] = videos

        except Exception as e:
            back_data['error'] = f"获取视频列表失败: {str(e)}"

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)

    def get_video_detail(self, args: Dict[str, Any]) -> str:
        """
        获取视频详情
        对应原JS的getVideoDetail函数

        Args:
            args: 包含url参数的字典
        """
        # 提取参数
        video_url = args.get('url', '')

        # 处理URL
        if not video_url.startswith('http'):
            if video_url.startswith('/'):
                full_url = self.base_url + video_url
            else:
                full_url = self.base_url + '/' + video_url
        else:
            full_url = video_url

        # 创建响应对象
        back_data = {
            'data': None,
            'error': None
        }

        try:
            response = self.session.get(full_url, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                back_data['error'] = f"请求失败，状态码: {response.status_code}"
                return json.dumps(back_data, ensure_ascii=False)

            soup = BeautifulSoup(response.text, 'html.parser')
            video_detail = {
                'vod_id': video_url,
                'panUrls': []  # 网盘链接列表
            }

            # 提取视频标题
            title_element = soup.select_one('.page-title')
            if title_element and title_element.contents:
                video_detail['vod_name'] = title_element.contents[0].strip()

            # 提取封面图
            cover_element = soup.select_one('.mobile-play .lazyload')
            if cover_element and cover_element.get('data-src'):
                video_detail['vod_pic'] = cover_element['data-src']

            # 提取视频信息项
            info_items = soup.select('.video-info-itemtitle')

            for item in info_items:
                key = item.get_text(strip=True)
                next_sibling = item.find_next_sibling()

                if not next_sibling:
                    continue

                if '剧情' in key:
                    # 提取剧情简介
                    content_element = next_sibling.find('p')
                    if content_element:
                        video_detail['vod_content'] = content_element.get_text(strip=True)

                elif '导演' in key:
                    # 提取导演信息
                    directors = []
                    director_links = next_sibling.find_all('a')
                    for link in director_links:
                        director_text = link.get_text(strip=True)
                        if director_text:
                            directors.append(director_text)
                    if directors:
                        video_detail['vod_director'] = ', '.join(directors)

                elif '主演' in key:
                    # 提取演员信息
                    actors = []
                    actor_links = next_sibling.find_all('a')
                    for link in actor_links:
                        actor_text = link.get_text(strip=True)
                        if actor_text:
                            actors.append(actor_text)
                    if actors:
                        video_detail['vod_actor'] = ', '.join(actors)

            # 提取网盘链接 - 修复弃用警告
            pan_elements = soup.select('.module-row-info')
            for element in pan_elements:
                # 使用string=True替代text=True
                text_elements = element.find_all(string=True)
                for text in text_elements:
                    cleaned_text = text.strip()
                    if cleaned_text and len(cleaned_text) > 10:  # 过滤掉过短的文本
                        video_detail['panUrls'].append(cleaned_text)

            back_data['data'] = video_detail

        except Exception as e:
            back_data['error'] = f"获取视频详情失败: {str(e)}"

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)

    def get_video_play_url(self, args: Dict[str, Any]) -> str:
        """
        获取视频播放地址
        对应原JS的getVideoPlayUrl函数
        返回JSON字符串
        """
        # 创建空响应对象
        back_data = {
            'data': None,
            'error': None
        }

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)

    def search_video(self, args: Dict[str, Any]) -> str:
        """
        搜索视频
        对应原JS的searchVideo函数

        Args:
            args: 包含searchWord和page参数的字典
        """
        # 提取参数
        keyword = args.get('searchWord', '')
        page = args.get('page', 1)

        # URL编码关键词
        encoded_keyword = quote(keyword)

        url = f"{self.base_url}/index.php/vod/search/page/{page}/wd/{encoded_keyword}.html"

        # 创建响应对象
        back_data = {
            'data': [],
            'error': None
        }

        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                back_data['error'] = f"请求失败，状态码: {response.status_code}"
                return json.dumps(back_data, ensure_ascii=False)

            soup = BeautifulSoup(response.text, 'html.parser')
            videos = []

            # 查找搜索结果项
            search_items = soup.select('.module-search-item')

            for item in search_items:
                video_info = {}

                # 提取视频链接和标题
                link_element = item.select_one('.video-serial')
                if link_element:
                    video_info['vod_id'] = link_element.get('href', '')
                    video_info['vod_name'] = link_element.get('title', '')
                    video_info['vod_remarks'] = link_element.get_text(strip=True)

                # 提取封面图
                img_element = item.select_one('.module-item-pic img')
                if img_element:
                    video_info['vod_pic'] = img_element.get('data-src', '')

                if video_info:
                    videos.append(video_info)

            back_data['data'] = videos

        except Exception as e:
            back_data['error'] = f"搜索失败: {str(e)}"

        # 转换为JSON字符串
        return json.dumps(back_data, ensure_ascii=False)


class VideoCrawlerManager:
    """视频爬虫管理器 - 提供更友好的API接口"""

    def __init__(self, base_url: str = "http://www.miqk.cc"):
        self.crawler = VideoCrawler(base_url)

    def list_categories(self) -> str:
        """获取所有视频分类"""
        return self.crawler.get_class_list()

    def get_videos_by_category(self, category_id: str, page: int = 1) -> str:
        """根据分类获取视频列表"""
        args = {
            'url': category_id,
            'page': page
        }
        return self.crawler.get_video_list(args)

    def get_video_info(self, video_url: str) -> str:
        """获取视频详细信息"""
        args = {
            'url': video_url
        }
        return self.crawler.get_video_detail(args)

    def search(self, keyword: str, page: int = 1) -> str:
        """搜索视频"""
        args = {
            'searchWord': keyword,
            'page': page
        }
        return self.crawler.search_video(args)


# 使用示例
if __name__ == "__main__":
    # 创建爬虫实例
    crawler_manager = VideoCrawlerManager()

    print("=== 至臻视频爬虫示例 ===")

    # 1. 获取分类列表
    print("\n1. 获取视频分类:")
    categories_result = crawler_manager.list_categories()
    categories_data = json.loads(categories_result)

    if categories_data.get('data'):
        for category in categories_data['data']:
            print(f"  - {category['type_name']} (ID: {category['type_id']})")

    # 2. 获取电影分类的视频列表
    print("\n2. 获取电影分类第一页视频:")
    movies_result = crawler_manager.get_videos_by_category("1", 1)
    movies_data = json.loads(movies_result)

    if movies_data.get('data'):
        print(f"找到 {len(movies_data['data'])} 个视频")
        for i, video in enumerate(movies_data['data'][:3]):  # 只显示前3个
            print(f"  {i + 1}. {video.get('vod_name', '未知')} - {video.get('vod_remarks', '')}")

    # 3. 搜索视频示例
    print("\n3. 搜索'爱情'相关视频:")
    search_result = crawler_manager.search("爱情", 1)
    search_data = json.loads(search_result)

    if search_data.get('data') and search_data['data']:
        video_url = search_data['data'][0].get('vod_id')
        if video_url:
            # 4. 获取第一个搜索结果的详情
            print("获取第一个搜索结果的详情:")
            detail_result = crawler_manager.get_video_info(video_url)
            detail_data = json.loads(detail_result)

            if detail_data.get('data'):
                detail = detail_data['data']
                print(f"  标题: {detail.get('vod_name', '未知')}")
                print(f"  导演: {detail.get('vod_director', '未知')}")
                print(f"  主演: {detail.get('vod_actor', '未知')}")
                print(f"  简介: {detail.get('vod_content', '无')[:100]}...")
                print(f"  网盘链接数: {len(detail.get('panUrls', []))}")

