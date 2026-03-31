import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import random
from base.spider import Spider
import urllib.parse
import re
class Spider(Spider):
    def init(self, extend=""):
        self.host = 'https://jciyuan.com'
    def get_headers(self, url):
        return {
    'user-agent':'Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'referer':'https://jciyuan.com/',
    'cookie':'HWTOKEN=cecf5e608cec99abe905e4715e5ea9c03ee4fa20e7954e14702fd83dce66ed2d; HWIDHASH=936f29746732961da43766a0f1c368fc; mx_style=black; showBtn=true; PHPSESSID=bhg28fus5hhm5t3ggshaqli518; user_id=34574; user_name=cn6666; group_id=2; group_name=%E9%BB%98%E8%AE%A4%E4%BC%9A%E5%91%98; user_check=bc7c259a922f2df0ec570b76060597c1; user_portrait=%2Fstatic%2Fimages%2Ftouxiang.png; mac_history_mxpro=%5B%7B%22vod_name%22%3A%22%E4%BB%99%E9%80%86%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F55-4-1.html%22%2C%22vod_part%22%3A%221%22%7D%2C%7B%22vod_name%22%3A%22%E5%90%9E%E5%99%AC%E6%98%9F%E7%A9%BA%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F32-4-97.html%22%2C%22vod_part%22%3A%2297%22%7D%2C%7B%22vod_name%22%3A%22%E6%AD%A6%E7%A5%9E%E4%B8%BB%E5%AE%B0%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F20-6-1.html%22%2C%22vod_part%22%3A%221%22%7D%2C%7B%22vod_name%22%3A%22%E9%80%86%E5%A4%A9%E8%87%B3%E5%B0%8A%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F42-3-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E4%B9%9D%E9%98%B3%E6%AD%A6%E7%A5%9E%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F36775-4-1.html%22%2C%22vod_part%22%3A%221%22%7D%5D'
    }


    def homeContent(self, filter):
        return {'class': [{"type_id": "21", "type_name": "ce"}

                          ]}


    def homeVideoContent(self): pass

    # 分类
    def categoryContent(self, tid, pg, filter, extend):
        url=f'{self.host}/acgshow/{tid}--------{pg}---.html'
        res = self.fetch(url, headers=self.get_headers(url), timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        all = soup.find('div', class_="module-main module-page")
        vod=[]
        for each in all.find_all('a'):
            try:
                href = each.get('href')
                name = each.get('title')
                rem = each.find('div', class_="module-item-note")
                pic = each.find('img').get('data-original')
            except:
                href = ''
                name = ''
                rem = ''
                pic = ''
            vod.append({
                'vod_id': href,
                'vod_name': name,
                'vod_pic': pic,
                'vod_remarks': rem
            })
        return {'list': vod, 'page': 5, 'pagecount': 10, 'limit': 10, 'total': 10}

    def detailContent(self, ids):
        url=self.host+ids[0]
        res = self.fetch(url, headers=self.get_headers(url), timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        all = soup.find(id="y-playList")
        ww = all.find_all('div', class_="module-tab-item tab-item")
        xl = []
        for i in ww:
            xlm = i.get('data-dropdown-value')
            xl.append(xl)
        all2 = soup.find_all('div', class_="module-play-list")
        box2 = []
        for index, ii in enumerate(all2):
            box1 = []
            for j in ii.find_all('a'):
                name = j.find('span').text
                href = j.get('href')
                url = f'{name}${href}'
                box1.append(url)
            play_url = '#'.join(box1)
            box2.append(play_url)
        play_urls = '$$$'.join(box2)
        vod = {
            "vod_id": ids[0],
            "vod_name": '',
            "vod_pic": '',
            "vod_play_from": '$$$'.join(xl),
            "vod_play_url": play_urls,
            "vod_content": 'py爬虫(伊)'
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):pass

    # 播放
    def playerContent(self, flag, id, vipFlags):
        url=self.host+id
        res = self.fetch(url, headers=self.get_headers(url), timeout=10)
        html_content = res.text
        # 1. 先定位 player_aaaa 赋值语句开始的位置
        # 2. 往后截取一段足够长的字符串（比如 5000 字符），确保包含完整的配置
        start_pos = html_content.find('player_aaaa')
        if start_pos != -1:
            # 截取从 player_aaaa 开始到后面一段内容，直到脚本结束标记 </script>
            end_pos = html_content.find('</script>', start_pos)
            if end_pos == -1:
                end_pos = start_pos + 5000

            block = html_content[start_pos:end_pos]

            # 3. 在这个块里用正则精准提取 url 的值
            # 这个正则支持: "url":"...", 'url':'...', url:"..." 各种写法
            # [^"']+ 表示匹配直到遇到下一个引号为止
            url_match = re.search(r'["\']?url["\']?\s*:\s*["\']([^"\'\s]+)["\']', block)

            if url_match:
                raw_url = url_match.group(1)

                # 4. 清理可能存在的转义反斜杠 (比如 \/ 替换成 /)
                raw_url = raw_url.replace('\\/', '/')

                # 5. URL 解码
                final_url = urllib.parse.unquote(raw_url)
        play_url = 'https://bfq.lggys.com/player?url=' + final_url
        result = {
            "parse": 1,
            "url":play_url,
            "timeout": 60
        }
        return result

    def isVideoFormat(self, url): pass

    # 视频检测
    def manualVideoCheck(self): pass


