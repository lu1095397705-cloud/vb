import random
import re
import base64
import time
import json
from base.spider import Spider


class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://qqqys.com'
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
        return {'class': [{"type_id": "1", "type_name": "电影"},
                          {"type_id": "2", "type_name": "剧集"},
                          {"type_id": "3", "type_name": "动漫"},
                          {"type_id": "4", "type_name": "综艺"}
                          ]}

    def categoryContent(self, tid, pg, filter, extend):
        url = f'{self.host}/api.php/web/filter/vod?type_id={tid}&page={pg}&sort=hits'
        try:
            time.sleep(random.uniform(1.3, 4.2))
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            if res.cookies.get_dict():
                self.cookies.update(res.cookies.get_dict())
            try:
                # 2. 解析 JSON 数据 (关键点)
                res_json = res.json()
                data_list = res_json.get('data', [])

                vod = []
                # 3. 循环提取字段
                for item in data_list:
                    vod.append({
                        "vod_id": str(item.get('vod_id')),
                        "vod_name": item.get('vod_name'),
                        "vod_pic": item.get('vod_pic'),
                        "vod_remarks": item.get('vod_remarks')
                    })
                return {
                    'list': vod,
                    'page': pg,
                    'pagecount': 10,
                    'total': 100
                }
            except Exception as e:
                print(f"解析出错: {e}")
                return {'list': []}
        except:
            return {'list': []}

    def detailContent(self, ids):
        try:
            vod_id = ids[0]
            # 1. 请求详情 API 获取线路和剧集信息
            url = f'https://qqqys.com/api.php/web/vod/get_detail?vod_id={vod_id}'
            res = self.fetch(url, headers=self.get_headers(url), cookies=self.cookies, timeout=10)
            res_json = json.loads(res.text)
            data = res_json.get('data', {})
            vod = {
                "vod_id": data.get('vod_id'),
                "vod_name": data.get('vod_name'),
                "vod_pic": data.get('vod_pic'),
                "type_name": data.get('type_name'),
                "vod_year": data.get('vod_year'),
                "vod_area": data.get('vod_area'),
                "vod_remarks": data.get('vod_remarks'),
                "vod_actor": data.get('vod_actor'),
                "vod_director": data.get('vod_director'),
                "vod_content": data.get('vod_content')
            }
            play_from = data.get('vod_play_from', '')
            play_url = data.get('vod_play_url', '')
            from_list = play_from.split('$$$')
            url_list = play_url.split('$$$')
            final_play_url = []
            for i in range(len(from_list)):
                sid = from_list[i]  # 线路名，如 BBA
                episodes = url_list[i].split('#')  # 拆分每一集
                ep_links = []
                for index, ep in enumerate(episodes):
                    if '$' in ep:
                        name = ep.split('$')[0]  # 比如 "第01集"
                    else:
                        name = f"第{index + 1}集"
                    # 关键点：我们将 nid (index+1) 和 sid 传给 playerContent
                    # 构造格式：视频ID|线路名|集数序号
                    combined_id = f"{vod_id}|{sid}|{index + 1}"
                    ep_links.append(f"{name}${combined_id}")

                final_play_url.append("#".join(ep_links))
            vod['vod_play_from'] = "$$$".join(from_list)
            vod['vod_play_url'] = "$$$".join(final_play_url)
            return {'list': [vod]}
        except Exception as e:
            self.log(f"Detail Error: {str(e)}")
            return {'list': []}

    def playerContent(self, flag, id, vipFlags):
        # 此时收到的 id 是我们在 detailContent 里拼凑的 "86474|BBA|2"

        try:
            parts = id.split('|')
            if len(parts) == 3:
                v_id, sid, nid = parts

                # 3. 构造出网页播放地址，例如：
                # https://qqqys.com/play/86474#sid=BBA&nid=2
                play_page_url = f"https://qqqys.com/play/{v_id}#sid={sid}&nid={nid}"

                self.log(f"【嗅探开始】目标网页: {play_page_url}")
                # 返回 parse: 1，TVBox 会自动打开这个网页并嗅探其中的视频流
                current_headers = self.get_headers(play_page_url)
                if self.cookies:
                    # 只有在 cookies 是字典时才需要 join
                    if isinstance(self.cookies, dict):
                        cookie_str = "; ".join([f"{k}={v}" for k, v in self.cookies.items()])
                        current_headers['Cookie'] = cookie_str
                    else:
                        current_headers['Cookie'] = self.cookies

                result = {
                    "parse": 1,
                    "url":play_page_url ,
                    "timeout": 60,
                    "header": current_headers
                }
        except Exception as e:
            self.log(f"Player Error: {str(e)}")
        return {'parse': 1, 'url': ''}