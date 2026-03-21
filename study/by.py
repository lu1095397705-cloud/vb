import requests
import json
from bs4 import BeautifulSoup

from tvbox.py.bebug import name

url = 'https://japi.zxfmj.com/api/v2/settings/homeCategory'
# https://japi.zxfmj.com/api/v2/settings/homeCategory
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

response = requests.get(url, headers=headers)
# print(response.json())
res=response.json()
wc=[]
for i in res.get("data",[]):
    id=i.get("id")
    name=i.get("name")
    li={"type_id": id, "type_name": name}
    wc.append(li)
print(wc)
























