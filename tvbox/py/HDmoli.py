import random
import re
import time
import json
from base.spider import Spider
from bs4 import BeautifulSoup


class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://hdmoli.org'
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
            res = self.fetch(self.host, headers=self.get_headers(self.host), timeout=15)
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
        return {'class': [{"type_id": "15", "type_name": "韩剧"},
                          {"type_id": "14", "type_name": "港台剧"},
                          {"type_id": "25", "type_name": "日韩漫"},
                          {"type_id": "26", "type_name": "港台漫"}
                          ]}

    def categoryContent(self, tid, pg, filter, extend):
        # 修复：pg 参数应该带入 URL
        url = f'{self.host}/show/{tid}--------{pg}---.html'
        try:

            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            tree = self.html(res.content)
            items = tree.xpath('//div[@class="myui-vodlist__box"]')
            vod = []
            for i in items:
                # 增加 try 保护，防止某一个视频解析失败导致整个列表为空
                try:
                    name = i.xpath('./a/@title')[0]
                    href = i.xpath('./a/@href')[0]
                    pic = i.xpath('./a/@data-original')[0]
                    # 有些影片没有备注，给个默认值
                    rem_list = i.xpath('./a/span[@class="pic-text text-left"]/text()')
                    rem = rem_list[0] if rem_list else ""
                    vod.append({
                        'vod_id': href,
                        'vod_name': name,
                        'vod_pic': pic,
                        'vod_remarks': rem,
                    })
                except:
                    continue
            return {'list': vod, 'page': 5, 'pagecount': 10, 'limit': 10, 'total': 10}
        except:
            return {'list': []}

    def detailContent(self, ids):
        # ids[0] 已经是 href 了（例如 /v/123.html）
        url = self.host + ids[0]
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        k = BeautifulSoup(res.text, 'lxml')
        xj = []
        mz = []
        ii = k.find('div', class_="myui-panel_bd clearfix")
        for i in ii.find_all('a'):
            name = i.get('title')
            play_url = i.get('href')
            xj.append(play_url)
            mz.append(name)
        play_urls = '$$$'.join(xj)
        names = '$$$'.join(mz)
        print(names)

        vod = {
            "vod_id": ids[0],
            "vod_name":'',
            "vod_pic":'',
            "vod_play_from": names,
            "vod_play_url": play_urls,
            "vod_content": "pbl少lu点"
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        url=f'{self.host}/search/-------------.html?wd={key}&submit='
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=15)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        tree = self.html(res.content)
        k = tree.xpath('//li[@class="clearfix"]')
        vod = []
        for g in k:
            i = g.xpath('.//div[@class="thumb"]')[0]
            name = i.xpath('./a/@title')[0]
            href = i.xpath('./a/@href')[0]
            pic = i.xpath('./a/@data-original')[0]
            vod.append({
                'vod_id': href,
                'vod_name': name,
                'vod_pic': pic,

            })
        result = {}
        result ['list'] = vod
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {
            "parse": 0,
            "url": "push://" + id,
        }

        return result
