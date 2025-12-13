
import requests
from lxml import etree
import re
import json
url = 'https://www.sunnafh.com/vod/show/id/fyclass/page/fypage'
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}
rep=requests.get(url, headers=headers)

i= etree.HTML(rep.text)
move_name=i.xpath('//div[@class="title"]/span/text()')
score=i.xpath('//div[@class="score __className_7bf612"]/text()')
k=list(zip(move_name,score))
with open('ce.text_file','a+',encoding='utf-8') as f:
    f.write(json.dumps(k,ensure_ascii=False))









