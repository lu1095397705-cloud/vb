import random
import re
import time
import json
from base.spider import Spider


class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://www.omofuna.com'
        self.cookies = {}
        self.ua_list = [
            # Chrome (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",

            # Chrome (macOS)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",

            # Edge (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",

            # Firefox (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",

            # Firefox (macOS)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",

            # Safari (macOS)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",

            # Mobile - iPhone (Safari)
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",

            # Mobile - Android (Chrome)
            "Mozilla/5.0 (Linux; Android 9; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",

            # iPad
            "Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1"
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
            'User-Agent': random.choice(self.ua_list),
            'Referer': self.host,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

    def homeContent(self, filter):
        return {'class': [{"type_id": "/type/2.html", "type_name": "国漫"}]}

    def categoryContent(self, tid, pg, filter, extend):
        url = f'{self.host}{tid}'
        try:
            time.sleep(random.uniform(1.3, 4.2))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            tree = self.html(res.content)
            k=tree.xpath('//div[@class="daFJ_dJJfFHa__gEI"]')
            vod = []
            for i in k:
                name=i.xpath('./a/@title')[0]
                href=i.xpath('./a/@href')[0]
                pic=i.xpath('./a/@data-original')[0]
                rem=i.xpath('./a/span[@class="aaE_EaDE text-right"]/text()')[0]
                vod.append({
                    'vod_id': href,
                    'vod_name': name,
                    'vod_pic': pic,
                    'vod_remarks': rem


            })
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
        k=tree.xpath('//li[@class="play-list-content-item show"]')
        playlist = []
        for q in k:
            vi=[]
            for i in q:
                pname = i.xpath('./a/@title')[0]
                purl = i.xpath('./a/@href')[0]
                purl = f'{pname}${purl}'
                vi.append(purl)
            xl='#'.join(vi)
        playlist.append(xl)
        vod = {
            "vod_id": ids[0],
            "vod_name":'',
            "vod_pic":'',
            "vod_play_from":'别看我，会陷进去$$$借个火，点燃心动',
            "vod_play_url":'$$$'.join(playlist),
            "vod_content":'测试'
          }


        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        pass
        # url = f''
        # time.sleep(random.uniform(2.2, 10.5))
        # res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        # if res.cookies.get_dict():
        #     self.cookies.update(res.cookies.get_dict())
        # tree = self.html(res.content)
        #
        # result = {}
        # result['list'] = vod
        # return result

    def playerContent(self, flag, id, vipFlags):
        url = self.host + id
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=20)

        # 修复：re.search 必须用字符串 (res.text) 而不是 tree 对象
        # 修复：正则修正
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
