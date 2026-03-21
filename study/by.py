import requests
import json
from bs4 import BeautifulSoup

from tvbox.py.bebug import name
tid=1
url =f'https://japi.zxfmj.com/api/dyTag/hand_data?category_id={tid}'
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

response = requests.get(url, headers=headers, timeout=10)
res = response.json()
data = res.get('data', {})
tid_map = {
    1: '32',
    2: '27',
    3: '13',
    88: '20'
}
key = tid_map.get(tid)
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
print(vod)
# response=requests.get(url,headers=self.headers,timeout=10)






















