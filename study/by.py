import requests
from bs4 import BeautifulSoup
url = 'https://rrys.lv/k/13-----------/'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36,'

}
response = requests.get(url, headers=headers)
print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
i = soup.find('div', class_="module-items module-poster-items-base")
vod = []
for k in i.find_all('a'):
    href = k.get('href')
    name = k.get('title')
    remark = k.find('div', class_="module-item-note").text
    img = k.find('img').get('data-original')
    if img:
        if not img.startswith('http'):
            img ='https://rrys.lv'+img
    vod.append({
        'vod_id': href,
        'vod_name': name,
        'vod_pic': img,
        'vod_remarks': remark
    })
print(vod)





