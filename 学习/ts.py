import requests
from lxml import etree
import csv
url = 'https://www.sunnafh.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/...'
}
resp = requests.get(url, headers=headers)
node=etree.HTML(resp.text)
tvbox_data = {
    "class": [],   # 分类列表
    "list": {}     # 按分类存储的影视列表
}
result_list=node.xpath('//div[@class="panel-item item"]')
data_list = []  # 用于存储所有数据的列表
for i in result_list :
    mv_name=i.xpath('//div[@class="title"]/span/text()')
    mv_img=i.xpath('//img/@src')
    mv_herf=i.xpath('//div[@class="content-card"]/a/@href')
    mv_content=i.xpath('//div[@class="bottom"]//text()')
    data_dict = {
        '名称': mv_name,
        '图片链接': mv_img,
        '详情链接': mv_herf,
        '内容': mv_content
    }
    data_list.append(data_dict)
    import json
    with open('ceshi.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)


















