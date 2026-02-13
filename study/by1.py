
import requests
from bs4 import BeautifulSoup
url='https://woog.nxog.eu.org/index.php/vod/detail/id/3225.html'
res=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'})
# print(res.content.decode('utf-8'))
resp = BeautifulSoup(res.content, 'html.parser')




















