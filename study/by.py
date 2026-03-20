import requests
from bs4 import BeautifulSoup
url = 'https://rrys.lv/rrvod/122538/'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36,'

}
response = requests.get(url, headers=headers)
print(response.text)
soup = BeautifulSoup(response.content, 'lxml')
xlm=soup.find(id="y-playList")
xlname=[]
for item in xlm.find_all('div', class_="module-tab-item tab-item"):
    names=item.get('data-dropdown-value')
    xlname.append(names)
xlnames='$$$'.join(xlname)
w=soup.find_all('div', class_='module-play-list')
playbox3=[]
for index,ji in enumerate(w):
    playbox1=[]
    for ji2 in ji.find_all('a', class_="module-play-list-link"):
        play_name = ji2.find('span').text
        play_href = ji2.get('href')
        play_url=f'{play_name}${play_href}'
        playbox1.append(play_url)
    playbox2='#'.join(playbox1)
    playbox3.append(playbox2)
playbox4="$$$".join(playbox3)




