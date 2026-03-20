import requests
from bs4 import BeautifulSoup
url = 'https://rrys.lv/s/-------------/?wd=%E5%89%91%E6%9D%A5'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36,'

}
response = requests.get(url, headers=headers)
# print(response.text)
soup=BeautifulSoup(response.text, 'lxml')
k=soup.find_all('div', class_="module-card-item module-item")
for ii in k:
    i=ii.find('a')
    href=i.get('href')
    name=i.find('img').get('alt')
    rem=i.find('div',class_="module-item-note").text
    pic=i.find('img').get('data-original')
    if pic:
        if not pic.startswith('http'):
            pic='https://rrys.lv'+pic








