import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'referer':'https://jciyuan.com/',
    # 'cookie':'HWTOKEN=cecf5e608cec99abe905e4715e5ea9c03ee4fa20e7954e14702fd83dce66ed2d; HWIDHASH=936f29746732961da43766a0f1c368fc; mx_style=black; showBtn=true; PHPSESSID=bhg28fus5hhm5t3ggshaqli518; user_id=34574; user_name=cn6666; group_id=2; group_name=%E9%BB%98%E8%AE%A4%E4%BC%9A%E5%91%98; user_check=bc7c259a922f2df0ec570b76060597c1; user_portrait=%2Fstatic%2Fimages%2Ftouxiang.png; mac_history_mxpro=%5B%7B%22vod_name%22%3A%22%E4%BB%99%E9%80%86%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F55-4-1.html%22%2C%22vod_part%22%3A%221%22%7D%2C%7B%22vod_name%22%3A%22%E5%90%9E%E5%99%AC%E6%98%9F%E7%A9%BA%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F32-4-97.html%22%2C%22vod_part%22%3A%2297%22%7D%2C%7B%22vod_name%22%3A%22%E6%AD%A6%E7%A5%9E%E4%B8%BB%E5%AE%B0%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F20-6-1.html%22%2C%22vod_part%22%3A%221%22%7D%2C%7B%22vod_name%22%3A%22%E9%80%86%E5%A4%A9%E8%87%B3%E5%B0%8A%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F42-3-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E4%B9%9D%E9%98%B3%E6%AD%A6%E7%A5%9E%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F36775-4-1.html%22%2C%22vod_part%22%3A%221%22%7D%5D'

}
url='https://jciyuan.com/acgsearch/%E4%BB%99%E9%80%86-------------.html'
res =requests.get(url, headers=headers,timeout=10)
# print(res.text)
soup = BeautifulSoup(res.text, 'lxml')
kk = soup.find_all('div', class_="module-card-item module-item")
for each in kk:
    name=each.find('img').get('alt')
    pic=each.find('img').get('data-original')
    rem=each.find('div', class_="module-item-note").text
    href=each.find('a').get('href')









