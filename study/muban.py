import random
import re
import time
import json
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
        return {'class': [{"type_id": "15", "type_name": "韩剧"}]}

    def categoryContent(self, tid, pg, filter, extend):
        # 修复：pg 参数应该带入 URL
        url = f''
        try:
            time.sleep(random.uniform(1.3, 4.2))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            tree = self.html(res.content)

            vod = []

            return {'list': vod, 'page': 5, 'pagecount': 10, 'limit': 10, 'total': 10}
        except:
            return {'list': []}

    def detailContent(self, ids):
        # ids[0] 已经是 href 了（例如 /v/123.html）
        url = self.host + ids[0]
        time.sleep(random.uniform(1.6, 6.3))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        tree = self.html(res.content)

        vod = {
        "vod_id": ids[0],
        "vod_name":,
        "vod_pic":,
        "vod_play_from":,
        "vod_play_url":,
        "vod_content":
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        url = f''
        time.sleep(random.uniform(2.2, 10.5))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        tree = self.html(res.content)
        result = {}
        result['list'] = vod
        return result

    def playerContent(self, flag, id, vipFlags):
        url = self.host + id
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=20)

        match = re.search(r'"url":"(http[^"]+)"', res.text)
        if not match:
            match = re.search(r"url\s*:\s*'(http[^']+)'", res.text)

        # 构建给播放器的 Header
        current_headers = self.get_headers(url)
        if self.cookies:
            # 关键：将 cookie 字典转为字符串
            cookie_str = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
            current_headers['Cookie'] = cookie_str

        result = {
            "parse": 1,
            "url": url,
            "timeout": 60,
            "header": current_headers
        }

        if match:
            real_url = match.group(1).replace('\\/', '/')
            if '.m3u8' in real_url.lower() or '.mp4' in real_url.lower():
                result["parse"] = 0
                result["url"] = real_url

        return result
