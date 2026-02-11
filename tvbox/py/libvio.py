import random
import re
import time
import json
from base.spider import Spider


class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://www.libvio.site/'
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
        return {'class': [{"type_id": "15", "type_name": "韩剧"}]}

    def categoryContent(self, tid, pg, filter, extend):
        # 修复：pg 参数应该带入 URL
        url = f'{self.host}/type/{tid}.html'
        try:
            time.sleep(random.uniform(1.3, 4.2))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            tree = self.html(res.content)
            items = tree.xpath('//div[@class="stui-vodlist__box"]')
            vod = []
            for i in items:
                # 增加 try 保护，防止某一个视频解析失败导致整个列表为空
                try:
                    name = i.xpath('.//a/@title')[0]
                    href = i.xpath('.//a/@href')[0]
                    pic = i.xpath('.//a/@data-original')[0]
                    # 有些影片没有备注，给个默认值
                    rem_list = i.xpath('.//a/span[@class="pic-text text-right"]/text()')
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
        url = self.host + ids[0]
        time.sleep(random.uniform(1.6 ,6.3))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        tree = self.html(res.content)

        from_nodes = tree.xpath('//h3[@class="iconfont icon-iconfontplay2"]//text()')

        # 2. 提取播放列表
        playlist_divs = tree.xpath('//ul[@class="stui-content__playlist clearfix"]')
        url_list = []
        for div in playlist_divs:
            episodes = []
            for a in div:
                name = a.xpath('./a/text()')[0]
                href = a.xpath('./a/@href')[0]
                episodes.append(f"{name}${href}")
            url_list.append("#".join(episodes))

        # 如果抓到的线路名和列表数量不符，自动生成线路名
        if len(from_nodes) != len(url_list):
            from_nodes = [f"线路{i + 1}" for i in range(len(url_list))]

        vod = {
            "vod_id": ids[0],
            "vod_name": '',
            "vod_pic": '',
            "vod_play_from": "$$$".join(from_nodes),
            "vod_play_url": "$$$".join(url_list),
            "vod_content": "抓取自hdmoli"
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        url=f'{self.host}/search/-------------.html?wd={key}'
        time.sleep(random.uniform(2.2, 10.5))
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
        if res.cookies.get_dict():
            self.cookies.update(res.cookies.get_dict())
        tree = self.html(res.content)
        k = tree.xpath('//div[@class="stui-vodlist__box"]')
        vod = []
        for i in k:
            name = i.xpath('.//a/@title')[0]
            href = i.xpath('.//a/@href')[0]
            pic = i.xpath('.//a/@data-original')[0]
            vod.append({
                'vod_id': href,
                'vod_name': name,
                'vod_pic': pic,

            })
        result = {}
        result ['list'] = vod
        return result

    def playerContent(self, flag, id, vipFlags):
        url = self.host + id
        res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=20)

        match = re.search(r'"url":"(http[^"]+)"', res.text)
        if not match:
            match = re.search(r'"url_next":"(http[^"]+)"',res.text)




        # 构建给播放器的 Header
        current_headers = self.get_headers(url)
        if self.cookies:
            # 只有在 cookies 是字典时才需要 join
            if isinstance(self.cookies, dict):
                cookie_str = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
                current_headers['Cookie'] = cookie_str
            else:
                current_headers['Cookie'] = self.cookies

        result = {
            "parse": 1,
            "url": url,
            "timeout": 60,
            "header": current_headers
        }

        if match:
            real_url = match.group(1).replace('\\/', '/')
            video_extensions = ('.m3u8', '.mp4', '.flv', '.mkv', '.avi')  # 甚至可以多加几个
            if any(ext in real_url.lower() for ext in video_extensions):
                result["parse"] = 0
                result["url"] = real_url


        return result