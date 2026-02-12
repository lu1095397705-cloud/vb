import random
import re
import time
import json
from base.spider import Spider
from bs4 import BeautifulSoup


class Spider(Spider):

    def init(self, extend=""):
        self.host = 'http://www.miqk.cc'
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
        return {'class': [
            {
                'type_id': '26',
                'type_name': '至臻严选'

            },
            {
            'type_id': '1',
            'type_name': '至臻电影'
        },
        {
            'type_id': '2',
            'type_name': '至臻剧集'

        },
        {
            'type_id': '3',
            'type_name': '至臻动漫'

        },
        {
            'type_id': '4',
            'type_name': '至臻综艺'

        },
        {
            'type_id': '5',
            'type_name': '至臻短剧'

        },
        {
            'type_id': '24',
            'type_name': '至臻老剧'

        }

                          ]
                }

    def categoryContent(self, tid, pg, filter, extend):
        url = f'{self.host}/index.php/vod/type/id/{tid}/page/{pg}.html'
        try:
            time.sleep(random.uniform(0.3, 2.2))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            resp=BeautifulSoup(res.text, 'html.parser')
            vod = []
            for i in resp.find_all('div', class_='module-item'):
                name=i.find('div', class_='module-item-pic').find('a').get('title')
                href=i.find('div', class_='module-item-pic').find('a').get('href')
                pic=i.find('img', class_="lazy lazyloaded").get('data-src')
                rem=i.find('div', class_="module-item-text").text
                vod.append({
                    'vod_id': href,
                    'vod_name': name,
                    'vod_pic': pic,
                    'vod_remarks': rem,
                })
            return {'list': vod, 'page': 5, 'pagecount': 10, 'limit': 10, 'total': 10}
        except:
            return {'list': []}

    def detailContent(self, ids):
        url = self.host + ids[0]
        time.sleep(random.uniform(1.6, 6.3))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        resp = BeautifulSoup(res.content, 'html.parser')
        href = []
        for i in resp.find_all('div', class_="module-row-shortcuts"):
            url = i.find('a').get('href')
            href.append(url)
        play_url = '$$$'.join(href)
        xll = []
        div_list = resp.find_all('div', class_='module-tab-content')
        if len(div_list) >= 2:
            second_div = div_list[1]
            spans = second_div.find_all('span')
            names = []
            for span in spans:
                val = span.get('data-dropdown-value')
                if val:
                    names.append(val)
            play_name = '$$$'.join(names)

        vod = {
        "vod_id": ids[0],
        "vod_name":'',
        "vod_pic":'',
        "vod_play_from":play_name,
        "vod_play_url":play_url,
        "vod_content":'抓取自木偶网盘,(伊)点第1集跳转到推送才能播放(学习交流，请勿非法用途)'
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        url = f'{self.host}/index.php/vod/search/page/{pg}/wd/{key}.html'
        time.sleep(random.uniform(2.2, 10.5))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        resp = BeautifulSoup(res.text, 'html.parser')
        vod = []
        for i in resp.find_all('div', class_='module-search-item'):
            name = i.find('a', class_="video-serial").get('title')
            href = i.find('a', class_="video-serial").get('href')
            pic = i.find('img', class_="lazy lazyload").get('data-src')
            rem = i.find('a', class_="video-serial").text
            vod.append({
                'vod_id': href,
                'vod_name': name,
                'vod_pic': pic,
                'vod_remarks': rem,
            })
        result = {}
        result['list'] = vod
        return result

    def playerContent(self, flag, id, vipFlags):

        result = {
            "parse": 0,
            "url":"push://" + id,
        }



        return result
