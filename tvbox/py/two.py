import random
import re
import time
import json
from base.spider import Spider
from bs4 import BeautifulSoup
class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://www.bttwo.me'
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
            {"type_id": "/hot-month", "type_name": "本月热门"},
            {"type_id": "/zgjun", "type_name": "国产"},
            {"type_id": "/jpsrtv", "type_name": "日韩"}

            ]}

    def categoryContent(self, tid, pg, filter, extend):
        # 修复：pg 参数应该带入 URL
        url = f'{self.host}{tid}'
        try:
            time.sleep(random.uniform(1.3, 4.2))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            soup = BeautifulSoup(res.content, 'html.parser')
            # 1. 先找到包含所有电影的 div
            ww = soup.find('div', class_="bt_img mi_ne_kd mrb")
            vod = []
            # 2. 遍历每一个 <li> 标签（每个 li 代表一部电影）
            for li in ww.find_all('li'):
                # 在这个 li 里面寻找我们需要的信息
                a_tag = li.find('a')
                img_tag = li.find('img', class_="thumb lazy")
                if a_tag and img_tag:
                    href = a_tag.get('href')
                    name = img_tag.get('alt')
                    pic = img_tag.get('data-original')

                    # 提取更新状态/备注 (class="jidi")
                    rem_div = li.find('div', class_="jidi")
                    rem = ""
                    if rem_div:
                        # 这里的 .text 可以直接获取所有内部文字
                        rem = rem_div.get_text(strip=True)

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
        url=ids[0]
        time.sleep(random.uniform(1.6, 6.3))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        resp = BeautifulSoup(res.content, 'html.parser')
        ww = resp.find('div', class_="paly_list_btn")
        play_url = []
        for a in ww.find_all('a'):
            href = a.get('href')
            name = a.text
            qq = f'{name}${href}'
            play_url.append(qq)
        vod = {
        "vod_id": ids[0],
        "vod_name":'',
        "vod_pic":'',
        "vod_play_from":'伊个大西瓜',
        "vod_play_url":'#'.join(play_url),
        "vod_content":'抓取自two点'
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        url = f'{self.host}/xssssearch?q={key}'
        time.sleep(random.uniform(2.2, 10.5))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        soup = BeautifulSoup(res.content, 'html.parser')
        # 1. 先找到包含所有电影的 div
        ww = soup.find('div', class_="bt_img mi_ne_kd search_list")
        vod = []
        # 2. 遍历每一个 <li> 标签（每个 li 代表一部电影）
        for li in ww.find_all('li'):
            # 在这个 li 里面寻找我们需要的信息
            a_tag = li.find('a')
            img_tag = li.find('img', class_="thumb lazy")
            if a_tag and img_tag:
                href = a_tag.get('href')
                name = img_tag.get('alt')
                pic = img_tag.get('data-original')
                # 提取更新状态/备注 (class="jidi")
                rem_div = li.find('div', class_="jidi")
                rem = ""
                if rem_div:
                    # 这里的 .text 可以直接获取所有内部文字
                    rem = rem_div.get_text(strip=True)

                vod.append({
                    'vod_id': href,
                    'vod_name': name,
                    'vod_pic': pic,
                    'vod_remarks': rem
                })
        result = {}
        result['list'] = vod
        return result

    def playerContent(self, flag, id, vipFlags):
        video_rule = r"\.(m3u8|mp4|flv|m4a|avi)([?!#].*)?$"

        # 最新的电脑端 Chrome User-Agent (Windows 版)
        pc_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

        return {
            'parse': 1,
            'url': id,
            'jx': 0,
            'timeout': 60,
            'rule': video_rule,
            'header': {
                'User-Agent': pc_ua,
                'Origin': 'https://www.bttwo.me',
                'Referer': 'https://www.bttwo.me/',  # 建议加上这个，防止视频地址失效
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
        }
