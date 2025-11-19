import requests
from lxml import etree
import json

# ---------------------- 1. 配置数据源和解析接口 ----------------------
target_url = "https://www.sunnafh.com/"  # 替换为你要抓取的影视网页
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# ---------------------- 2. 抓取网页数据 ----------------------
resp = requests.get(target_url, headers=headers)
i  = etree.HTML(resp.text)

# ---------------------- 3. 构造TVBox格式的JSON结构 ----------------------
tvbox_data = {
    "class": [],   # 分类列表
    "list": {}     # 按分类存储的影视列表
}

# ---------- 示例：假设分为“电影”和“电视剧”两类，需根据实际网页结构调整XPath ----------
# 电影分类处理
movie_nodes = i.xpath('//div[@class="panel-item item"]')  # 替换为实际网页中电影条目的XPath
movie_list = []
for i in movie_nodes:
    mv_name = i .xpath('//div[@class="title"]/span/text()')[0].strip()  # 替换为名称的XPath
    mv_play_url = i .xpath('//div[@class="content-card"]/a/@href')[0].strip()  # 替换为播放源的XPath
    mv_pic = i .xpath('//img/@src')[0].strip()  # 替换为封面的XPath（可选）
    movie_list.append({
        "name": mv_name,
        "url":  mv_play_url,  # 拼接解析接口

    })
tvbox_data["class"].append({"type": "电影", "id": "movie"})
tvbox_data["list"]["movie"] = movie_list


# ---------------------- 4. 生成JSON文件 ----------------------
with open("tvbox_data.json", "w", encoding="utf-8") as f:
    json.dump(tvbox_data, f, ensure_ascii=False, indent=2)
print("TVBox格式的JSON文件已生成：tvbox_data.json")