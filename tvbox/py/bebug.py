import requests
from bs4 import BeautifulSoup
url='https://hdmoli.org/movie/index2635.html'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
}
res=requests.get(url,headers=headers)
# print(res.text)
k=BeautifulSoup(res.text,'lxml')
xj=[]
mz=[]
ii=k.find('div',class_="myui-panel_bd clearfix")
for i in ii.find_all('a'):
    name=i.get('title')
    play_url=i.get('href')
    xj.append(play_url)
    mz.append(name)
play_urls='$$$'.join(xj)
names='$$$'.join(mz)
print(names)

