import json
import requests
import urllib.parse
from base.spider import Spider

# 假设这是基类
class Spider(Spider):
    def __init__(self):
        pass


class Spider(Spider):
    def __init__(self):
        self.base_url = "https://ev5356.970xw.com"
        self.img_domain = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; V2196A Build/PQ3A.190705.08211809; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:416;packageName:com.jp3.xg3"
        }

    def getName(self):
        return "剪片"

    def init(self, extend=""):
        """复刻 Java 中的 init 逻辑：动态获取域名"""
        try:
            # 1. DNS解析获取后缀
            dns_res = requests.get("https://dns.alidns.com/resolve?name=swrdsfeiujo25sw.cc&type=TXT", timeout=5).json()
            if "Answer" in dns_res:
                raw_data = dns_res["Answer"][0]["data"].replace('"', '')
                suffixes = raw_data.split(",")
                for suffix in suffixes:
                    test_url = f"https://wangerniu.{suffix}"
                    # 2. 验证并获取资源域名配置
                    try:
                        cfg_resp = requests.get(f"{test_url}/api/v2/settings/resourceDomainConfig", timeout=3).json()
                        if cfg_resp.get("data"):
                            self.base_url = test_url
                            self.img_domain = cfg_resp["data"]["imgDomain"].split(",")[0]
                            break
                    except:
                        continue
        except:
            pass

    def get_headers(self):
        h = self.headers.copy()
        h["Referer"] = self.base_url
        return h

    # 首页分类
    def homeContent(self, filter):
        url = f"{self.base_url}/api/v2/settings/homeCategory"
        res = requests.get(url, headers=self.get_headers()).json()
        classes = []
        for item in res.get("data", []):
            name = item.get("name")
            if name != "推荐":
                classes.append({"type_id": str(item.get("id")), "type_name": name})
        return {"class": classes}

    # 推荐视频 (对应 Java 中的 homeVideoContent)
    def homeVideoContent(self):
        url = f"{self.base_url}/api/slide/list?pos_id=88"
        res = requests.get(url, headers=self.get_headers()).json()
        videos = []
        for item in res.get("data", []):
            videos.append({
                "vod_id": str(item.get("id")),
                "vod_name": item.get("title"),
                "vod_pic": self.img_domain + item.get("thumbnail", ""),
                "vod_remarks": item.get("last_episode_title", "")
            })
        return {"list": videos}

    # 分类列表 (Java 源码中此段被跳过，按常规 API 补全)
    def categoryContent(self, tid, pg, filter, extend):
        url = f"{self.base_url}/api/video/list?category_id={tid}&page={pg}&pageSize=20"
        res = requests.get(url, headers=self.get_headers()).json()
        videos = []
        for item in res.get("data", []):
            videos.append({
                "vod_id": str(item.get("id")),
                "vod_name": item.get("title"),
                "vod_pic": self.img_domain + item.get("thumbnail", ""),
                "vod_remarks": item.get("last_episode_title", "")
            })
        return {"list": videos, "page": pg, "pagecount": 999, "limit": 20, "total": 999}

    # 详情 (对应 Java 中的 detailContent)
    def detailContent(self, ids):
        vod_id = ids[0]
        url = f"{self.base_url}/api/video/detailv2?id={vod_id}"
        res = requests.get(url, headers=self.get_headers()).json()
        data = res.get("data", {})

        vod = {
            "vod_id": vod_id,
            "vod_name": data.get("title"),
            "vod_pic": self.img_domain + data.get("thumbnail", ""),
            "type_name": data.get("category_name"),
            "vod_year": data.get("year"),
            "vod_area": data.get("area"),
            "vod_content": data.get("description"),
            "vod_actor": data.get("actor", ""),
            "vod_director": data.get("director", "")
        }

        # 核心逻辑：解析多线路播放列表
        play_from = []
        play_url = []
        for source in data.get("list", []):  # Java a2.f()
            play_from.append(source.get("source_name", "线路"))
            urls = []
            for ep in source.get("episodes", []):  # Java bVar2.a()
                # 拼接格式: 集数名$播放地址
                urls.append(f"{ep.get('title')}${ep.get('url')}")
            play_url.append("#".join(urls))

        vod["vod_play_from"] = "$$$".join(play_from)
        vod["vod_play_url"] = "$$$".join(play_url)

        return {"list": [vod]}

    # 搜索 (对应 Java 中的 searchContent)
    def searchContent(self, key, quick):
        encoded_key = urllib.parse.quote(key)
        url = f"{self.base_url}/api/v2/search/videoV2?key={encoded_key}&category_id=88&page=1&pageSize=20"
        res = requests.get(url, headers=self.get_headers()).json()
        videos = []
        for item in res.get("data", []):
            videos.append({
                "vod_id": str(item.get("id")),
                "vod_name": item.get("title"),
                "vod_pic": self.img_domain + item.get("thumbnail", ""),
                "vod_remarks": item.get("last_episode_title")
            })
        return {"list": videos}

    # 播放 (对应 Java 中的 playerContent)
    def playerContent(self, flag, id, vipFlags):
        # 原 Java 代码中 playerContent 只是简单的把 id 传回，并带上 Headers
        return {
            "parse": 0,
            "url": id,  # 这里的 id 其实就是 detail 里拿到的 url
            "header": self.get_headers()
        }