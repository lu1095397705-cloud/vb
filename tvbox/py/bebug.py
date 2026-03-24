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
url = f'https://japi.zxfmj.com/api/v2/search/videoV2?key=%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9&category_id=88&page=1&pageSize=20'
response =requests.get(url, headers=headers, timeout=10)
# print(response.text)
all = response.json()
alls = all.get('data', [])
vod=[]
for item in alls:
    name=item.get('title')
    id=item.get('id')
    rem=item.get('mask')
    pic=item.get('tvimg')
    if pic:
        if not pic.startswith('http'):
            pic = 'https://img.jgsfnl.com' + pic
    vod.append({
        'vod_id': id,
        'vod_name': name,
        'vod_pic': pic,
        'vod_remarks': rem
    })
print(vod)


