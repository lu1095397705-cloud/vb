
import requests
from bs4 import BeautifulSoup
url='https://666.666291.xyz/index.php/vod/detail/id/178.html'
res=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'})
# print(res.content.decode('utf-8'))
resp=BeautifulSoup(res.content,'html.parser')
href=[]
for i in resp.find_all('div',class_="module-row-shortcuts"):
    url = i.find('a').get('href')
    href.append(url)
play_url='$$$'.join(href)
xll=[]
div_list = resp.find_all('div', class_='module-tab-content')
if len(div_list) >= 2:
    second_div = div_list[1]
    spans = second_div.find_all('span')
    names = []
    for span in spans:
        val = span.get('data-dropdown-value')
        if val:
            names.append(val)
    play_name = '$$$'.join(names)
















