import random
import re
import time
import json
import urllib.parse
from base.spider import Spider


class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://movie.douban.com'
        self.cookies = {}
        self.ua_list = [
            "Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; V2242A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; PGT-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
        ]
        self.refresh_session()

    def refresh_session(self):
        try:
            res = self.fetch(self.host, headers=self.get_headers(self.host), timeout=10)
            if res and res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
        except:
            pass

    def get_headers(self, url):
        return {
            'user-Agent': random.choice(self.ua_list),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'referer': f'{self.host}/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def homeContent(self, filter):
        # 定义 TVBox 顶部分类。
        # 这里用 "类型_标签" 的格式作为 type_id，方便后面拆分给豆瓣接口用
        classes = [
            {"type_id": "movie_热门", "type_name": "热门电影"},
            {"type_id": "movie_豆瓣高分", "type_name": "高分电影"},
            {"type_id": "tv_热门", "type_name": "热门剧集"},
            {"type_id": "tv_国产剧", "type_name": "国产剧"},
            {"type_id": "tv_美剧", "type_name": "美剧"},
            {"type_id": "tv_韩剧", "type_name": "韩剧"},
            {"type_id": "tv_日本动画", "type_name": "热门动漫"},
            {"type_id": "tv_综艺", "type_name": "热门综艺"}
        ]
        return {'class': classes}

    def categoryContent(self, tid, pg, filter, extend):
        try:
            # 解析 tid，例如 "movie_热门" -> d_type="movie", d_tag="热门"
            d_type, d_tag = tid.split('_')
            limit = 20
            start = (int(pg) - 1) * limit

            # URL编码中文标签
            d_tag_encoded = urllib.parse.quote(d_tag)

            # 调用豆瓣 AJAX 加载接口
            url = f'{self.host}/j/search_subjects?type={d_type}&tag={d_tag_encoded}&page_limit={limit}&page_start={start}'

            # 适当延时防封
            time.sleep(random.uniform(0.5, 1.5))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)

            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())

            data = json.loads(res.text)
            vod_list = []

            for item in data.get('subjects', []):
                vod_list.append({
                    "vod_id":"push://search?wd=" + item.get('id'),  # 影片ID
                    "vod_name": item.get('title'),  # 标题
                    "vod_pic": item.get('cover'),  # 封面海报
                    "vod_remarks": f"评分: {item.get('rate')}"  # 右下角角标显示评分
                })

            return {'list': vod_list, 'page': int(pg), 'pagecount': 99, 'limit': limit, 'total': 999}
        except Exception as e:
            print(f"列表解析错误: {e}")
            return {'list': []}

    def detailContent(self, ids):
        pass

    def searchContent(self, key, quick, pg="1"):
        pass
    def playerContent(self, flag, id, vipFlags):
        pass