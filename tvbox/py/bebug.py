import requests
from bs4 import BeautifulSoup
headers = {
            "Host": "japi.zxfmj.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; PBBM00 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:424;packageName:com.lgvnqo.zniebv",
            "version": "427",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.9",
            "X-Requested-With": "com.lgvnqo.zniebv"
}
url = f'https://japi.zxfmj.com/api/video/detailv2?id='
response =requests.get(url, headers=headers, timeout=10)
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
    "vod_id":'',
    "vod_name": '',
    "vod_pic": '',
    "vod_play_from": '$$$'.join(xlname),
    "vod_play_url": '$$$'.join(box),
    "vod_content": 'py爬虫(伊)'
}
print(vod)
