import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 全局配置
site_url = "https://www.miqk.cc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


def home():
    return {
        "class": [{"type_id": "", "type_name": "最新资源"}],
        "filters": {}
    }


def homeVideo():
    try:
        res = requests.get(site_url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        videos = []
        for item in soup.select('div.item')[:20]:
            a = item.select_one('a.title') or item.select_one('h3 a')
            img = item.select_one('img')
            if not a: continue
            title = a.get_text(strip=True)
            vid = a.get('href')
            pic = img.get('data-src') or img.get('src') if img else ''
            if vid and title:
                videos.append({
                    "vod_id": urljoin(site_url, vid),
                    "vod_name": title,
                    "vod_pic": urljoin(site_url, pic) if pic else '',
                    "vod_remarks": ""
                })
        return {"list": videos}
    except:
        return {"list": []}


def category(tid, pg, filter, extend):
    # 网盘站通常无分类，统一走首页
    return homeVideo()


def detail(vod_id):
    try:
        res = requests.get(vod_id, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        title = soup.select_one('h1') or soup.select_one('title')
        vod_name = title.get_text(strip=True) if title else "未知影片"

        # 提取所有可能的网盘链接
        links = []
        text = res.text

        # 匹配百度网盘、阿里云盘等
        patterns = [
            r'https?://pan\.baidu\.com/s/[a-zA-Z0-9_-]+',
            r'https?://www\.aliyundrive\.com/s/[a-zA-Z0-9_-]+',
            r'https?://www\.alipan\.com/s/[a-zA-Z0-9_-]+'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for link in matches:
                links.append(link)

        # 去重
        links = list(dict.fromkeys(links))

        play_list = "#".join([f"网盘资源{idx + 1}${link}" for idx, link in enumerate(links)])

        return {
            "list": [{
                "vod_id": vod_id,
                "vod_name": vod_name,
                "vod_play_from": "网盘",
                "vod_play_url": play_list
            }]
        }
    except:
        return {"list": []}


def search(wd, quick):
    try:
        search_url = f"{site_url}/index.php?m=vod-search&wd={wd}"
        res = requests.get(search_url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        videos = []
        for item in soup.select('div.item')[:20]:
            a = item.select_one('a.title') or item.select_one('h3 a')
            img = item.select_one('img')
            if not a: continue
            title = a.get_text(strip=True)
            vid = a.get('href')
            pic = img.get('data-src') or img.get('src') if img else ''
            if vid and title:
                videos.append({
                    "vod_id": urljoin(site_url, vid),
                    "vod_name": title,
                    "vod_pic": urljoin(site_url, pic) if pic else '',
                    "vod_remarks": ""
                })
        return {"list": videos}
    except:
        return {"list": []}


def playerUrl(flag, id, vipFlags):
    # 网盘链接直接返回，TVBox会调用解析器或跳转浏览器
    return {"url": id, "header": {}}