import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import random
from base.spider import Spider


class Spider(Spider):
    def init(self, extend=""):
        self.host = ''
        self.cookies = {}
        self.ua_list = [
            "Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; V2242A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; PGT-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
        ]
        self.refresh_session()

    def refresh_session(self):
        try:
            # 增加 timeout 防止连接超时卡死
            res = self.fetch(self.host, headers=self.get_headers(self.host), timeout=10)
            if res and res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
        except:
            pass

    def get_headers(self, url):
        return {
            'user-Agent': random.choice(self.ua_list),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="134", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': f'{self.host}/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'priority': 'u=0, i',
        }

    def homeContent(self, filter):
        return {'class': [{"type_id": "13", "type_name": "电视剧"},
                          {"type_id": "31", "type_name": "国产动漫"},
                          {"type_id": "4", "type_name": "动漫"},
                          {"type_id": "1", "type_name": "电影"},
                          {"type_id": "14", "type_name": "港台"},
                          {"type_id": "4", "type_name": "综艺"},
                          {"type_id": "33", "type_name": "韩剧"},
                          {"type_id": "15", "type_name": "小日本"}
                          ]}

    def homeVideoContent(self):
        pass

    # 分类
    def categoryContent(self, tid, pg, filter, extend):
        pass

    # 详情
    def detailContent(self, ids):
        pass

    # 搜索
    def searchContent(self, key, quick, pg="1"):
        pass

    # 播放
    def playerContent(self, flag, id, vipFlags):
        pass

    # 视频格式
    def isVideoFormat(self, url):
        pass

    # 视频检测
    def manualVideoCheck(self):
        pass


