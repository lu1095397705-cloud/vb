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
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; V2242A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
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

    def format_pic(self, pic_url):
        """修复海报无法显示的核心函数"""
        if not pic_url:
            return ""
        # 1. 强制将 webp 替换为 jpg，解决老旧电视盒子无法显示图片的问题 (豆瓣CDN自带jpg转换)
        pic_url = pic_url.replace('.webp', '.jpg')
        # 2. TVBox 专属语法：在图片URL后加上 @Referer=... 绕过豆瓣的图片防盗链(403)
        if "@" not in pic_url:
            pic_url = pic_url + "@Referer=https://movie.douban.com/"
        return pic_url

    def homeContent(self, filter):
        # 顶部分类。使用 "类型_标签" 格式，方便 categoryContent 拆分调用接口
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
            d_type, d_tag = tid.split('_', 1)
            limit = 20
            start = (int(pg) - 1) * limit
            d_tag_encoded = urllib.parse.quote(d_tag)
            url = f'{self.host}/j/search_subjects?type={d_type}&tag={d_tag_encoded}&page_limit={limit}&page_start={start}'
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())

            data = json.loads(res.text)
            vod_list = []

            for item in data.get('subjects', []):
                # 兼容提取 cover、pic、img 字段
                raw_pic = item.get('cover') or item.get('pic') or item.get('img') or ""


                vod_list.append({
                    "vod_id":'',
                    "vod_name": item.get('title'),
                    "vod_pic": self.format_pic(raw_pic),  # 调用图片修复函数
                    "vod_remarks": f"评分: {item.get('rate')}"
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

