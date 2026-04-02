import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'referer':'http://www.miqk.cc/',

}
url='http://www.miqk.cc/index.php/vod/detail/id/6139.html'
res =requests.get(url, headers=headers,timeout=10)
# print(res.text)
soup=BeautifulSoup(res.text,'lxml')
nall=soup.find_all('div', class_="module-tab-content")
namebox=[]
for i in nall:
    try:
        ii = i.find_all('span')
        for j in ii:
            lxm=j.text
            if lxm:
                if lxm.startswith(('夸克','百度')):
                    namebox.append(lxm)

    except:
        continue
play_name='$$$'.join(namebox)
print(play_name)


















