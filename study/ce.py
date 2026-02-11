import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote
import time
import random
from base.spider import Spider
import urllib



class Spider(Spider):

    def init(self, extend=""):
        self.session = requests.Session()
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.ntdm8.com/",
            "Origin": "https://www.ntdm8.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1"
        }

        self.session.headers.update(self.header)

    def homeContent(self, filter):
        result = {}
        result['class'] = [
            {"type_id": "zhongguo", "type_name": "中国"},
            {"type_id": "riben", "type_name": "小日本去死日本"},
            {"type_id": "omei", "type_name": "欧美"}
        ]
        return result


    def homeVideoContent(self):
        return {}

    def categoryContent(self, tid, pg, filter, extend):
        time.sleep(random.uniform(2, 4))
        result = {}
        videos = []
        url = f"https://www.ntdm8.com/type/{tid}-{pg}.html"
        resp = self.session.get(url, timeout=10)
        html = resp.text
        # 关键改动：使用 'html.parser'，它在所有环境中都可用
        soup = BeautifulSoup(html, 'html.parser')
        for boxall in soup.find_all('div', class_='cell blockdif2'):
            a_tag = boxall.find('a')
            img_tag = boxall.find('img')
            remark_tag = boxall.find('span', class_='newname')
            # 安全检查：确保所有需要的标签都存在
            if not (a_tag and img_tag):
                continue
            vod_id = a_tag.get('href', '').replace('/video/', '').replace('.html', '')
            if not vod_id:
                continue
            videos.append({
                "vod_id": vod_id,
                "vod_name": img_tag.get('alt', '未知名称'),
                "vod_pic": img_tag.get('src', ''),
                "vod_remarks": remark_tag.text.strip() if remark_tag else ""
            })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 999
            result['limit'] = len(videos)
            result['total'] = 999
        return result

    def detailContent(self, ids):
        time.sleep(random.uniform(2, 4))
        vod_id = str(ids[0])
        url = "https://www.ntdm8.com" + vod_id

        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')

        ston = "https://www.ntdm8.com"
        play_boxs = soup.find_all('div', {'class': 'movurl mod'})

        vod_play_url = []
        for play_box in play_boxs:
            play_urls = []
            for a in play_box.find_all('a'):
                name = a.get('title')
                play_url = a.get('href')
                full_url = ston + play_url
                zh_ji = f'{name}${full_url}'
                play_urls.append(zh_ji)
            vod_play_url.append('#'.join(play_urls))
        vod_play_urls = "$$$".join(vod_play_url)

        vod = {
            "vod_id": vod_id,
            "vod_name": "",
            "vod_pic": "",
            "vod_remarks": "",
            "vod_content": "",
            "vod_play_from": "伊朵樱花送给你$$$两朵$$$三朵",
            "vod_play_url": vod_play_urls

        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        videos = []
        encoded_key = quote(key)
        url = "https://www.ntdm8.com/search/-------------.html?wd={}".format(encoded_key)
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for div in soup.find_all('div', class_="cell blockdif2"):
            name = div.find('img').get('alt')
            pic = div.find('img').get('src')
            content = div.find('span', class_="newname").text
            mid = div.find('a').get('href')

            videos.append({
                'vod_id': mid,
                'vod_name': name,
                'vod_pic': pic,
                'vod_remarks': content,
            })

        result={"list":videos, "page":pg}
        return result

    def playerContent(self, flag, id, vipFlags):
        url = id

        result = {
            "parse": 1,
            "playUrl": "",
            "url": url,
            "header": self.header
        }
        return result


