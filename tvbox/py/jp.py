from base.spider import Spider
import json
import requests
class Spider(Spider):
    def init(self, extend=""):
        self.host='https://japi.zxfmj.com'
        self.headers = {
            "Host": "japi.zxfmj.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; PBBM00 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:424;packageName:com.lgvnqo.zniebv",
            "version": "427",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.9",
            "X-Requested-With": "com.lgvnqo.zniebv"
        }
    def homeContent(self, filter):
        url=f'{self.host}/api/v2/settings/homeCategory'
        response =self.fetch(url, headers=self.headers, timeout=10)
        res = response.json()
        wc = []
        for i in res.get("data", []):
            id = i.get("id")
            name = i.get("name")
            li = {"type_id": id, "type_name": name}
            wc.append(li)
        return {'class':wc}


    def homeVideoContent(self): pass

    def categoryContent(self, tid, pg, filter, extend):
        try:
            tid_int = int(tid)
        except:
            tid_int = tid
        url=f'{self.host}/api/dyTag/hand_data?category_id={tid_int}'
        response=requests.get(url,headers=self.headers,timeout=10)
        res = response.json()
        data = res.get('data', {})
        tid_map = {
            1: '32',
            2: '27',
            3: '13',
            88:'20'
        }
        key = tid_map.get(tid_int)
        bl = data.get(key, []) if key else []
        vod = []
        for item in bl:
            href = item.get('id')
            rem = item.get('mask')
            name = item.get('title')
            pic = item.get('path')
            pics = pic.replace('\\/', '/')
            if pics:
                if not pic.startswith('http'):
                    pics = 'https://img.jgsfnl.com' + pics
            vod.append({
                'vod_id': href,
                'vod_name': name,
                'vod_pic': pics,
                'vod_remarks': rem
            })
        return {'list': vod, 'page': 5, 'pagecount': 10, 'limit': 10, 'total': 10}

    def detailContent(self, ids):
        id=ids[0]
        url=f'{self.host}/api/video/detailv2?id={id}'
        response=self.fetch(url,headers=self.headers,timeout=10)
        all = response.json()
        liall = all['data']['source_list_source']
        xlname = []
        for item in liall:
            lxm = item.get('name')
            xlname.append(lxm)
        box = []
        for ass in liall:
            lia = ass.get('source_list', [])
            urlbox = []
            for ki in lia:
                play_name = ki.get('source_name')
                play_url = ki.get('url')
                play_urls = play_url.replace('\\/', '/')
                play_box = f'{play_name}${play_url}'
                urlbox.append(play_box)
            urlbox2 = '#'.join(urlbox)
            box.append(urlbox2)
        vod = {
            "vod_id": ids[0],
            "vod_name": '',
            "vod_pic": '',
            "vod_play_from":'$$$'.join(xlname),
            "vod_play_url": '$$$'.join(box),
            "vod_content": 'py爬虫(伊)'
        }
        return {"list": [vod]}

    # 搜索
    def searchContent(self, key, quick): pass

    # 播放
    def playerContent(self, name, id, vip, flags):

        play_url_from_api = id

        # 2. 构造给播放器的 Header 字符串
        # 注意：一定要包含那个特殊的 User-Agent 和 X-Requested-With
        ua = "Mozilla/5.0 (Linux; Android 9; PBBM00 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:424;packageName:com.lgvnqo.zniebv"
        xr = "com.lgvnqo.zniebv"

        # 按照 TVBox 格式拼接
        # 如果 m3u8 内部还有多级跳转，建议把所有的 Header 都挂上
        header_params = f"#User-Agent={ua}&X-Requested-With={xr}"

        final_url = play_url_from_api + header_params

        return {
            "parse": 0,
            "url": final_url,
            "header": {
                "User-Agent": ua,
                "X-Requested-With": xr
            }
        }

    # 视频格式
    def isVideoFormat(self, url): pass

    # 视频检测
    def manualVideoCheck(self): pass

