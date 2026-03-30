import requests
from bs4 import BeautifulSoup
headers = {
    "x-aid": "com.sunshine.tv",
    "x-ave": "5",
    "x-time": "1774419217",
    "x-nonc": "659",
    "x-sign": "58A197F3018D9398D448D6ADC731AA927BC59508F2ED1321D46D43AAD18069DA",
    "user-agent": "okhttp/4.12.0",
    "accept": "application/json"
}
url='https://bubuyingshi.com/api.php/app/filter/vod?type_name=%E7%94%B5%E5%BD%B1&page=1&sort=hits'
response =requests.get(url, headers=headers,timeout=10)
all=response.json()
alls = all['data']['categories']








