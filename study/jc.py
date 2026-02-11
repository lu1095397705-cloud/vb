
import requests
from bs4 import BeautifulSoup
from base.spider import Spider


class Spider(Spider):
    def init(self, extend=""):
        self.host = "https://cn.xgcartoon.com"
        self.header = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Cookie':'_ga=GA1.0.amp-fhJb6TiaWLwxPu8_DrrnWg',
            'Referer': 'https://cn.xgcartoon.com/'
        }
        self.session = requests.session()
        self.session.headers.update(self.header)


    def homeContent(self, filter):
        result={}
        result['class'] = [
            {"type_id": "cn", "type_name": "国漫"}
        ]
        return result



    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        url=f'{self.host}/classify?type=%2a&region={tid}&state=%2a&filter=%2a'
        res=self.session.get(url,headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        video=[]
        result={}
        for li in soup.find_all('div', class_='col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-6 topic-list-box'):
            vod_id = li.find('a').get('href')
            vod_name = li.find('div', class_='h3 mb12').get_text(strip=True)
            vod_pic = li.find('amp-img').get('src')
            video.append({
                'vod_id':vod_id,
                'vod_name':vod_name,
                'vod_pic':vod_pic
            })
        result['list'] = video
        result['page'] = pg
        result['pagecount'] = 999
        result['limit'] = len(video)
        result['total'] = 999
        return result

    def detailContent(self, ids):
        vid=ids[0]
        url=f'{self.host}{vid}'
        res=self.session.get(url,headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        play_list = []
        for li in soup.find_all('div', class_='col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-6 col-6'):
            for k in li.find_all('a'):
                vod_url = k.get('href')
                vod_name = k.get('title')
                pj = f'{vod_name}${vod_url}'
                play_list.append(pj)
            yt = '#'.join(play_list)
        vod = {
            "vod_id": vid,
            "vod_name": "",
            "vod_pic": "",
            "vod_remarks": '',
            "vod_content": '本想送你一场春雨，可又怕湿了你的衣裳，最后只化作这一阵微风',
            "vod_play_from":'山水一程，三生有幸',
            "vod_play_url": yt
        }
        return {'list': [vod]}


    def searchContent(self, key, quick,pg="1"):
        url=f'https://cn.xgcartoon.com/search?q={key}'
        res=self.session.get(url,headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        video = []
        result = {}
        for li in soup.find_all('div', class_='col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-6 topic-list-box'):
            vod_id = li.find('a').get('href')
            vod_name = li.find('div', class_='h3 mb12').get_text(strip=True)
            vod_pic = li.find('amp-img').get('src')
            video.append({
                'vod_id': vod_id,
                'vod_name': vod_name,
                'vod_pic': vod_pic
            })
        result['list'] = video
        return result

    def playerContent(self, flag, id, vipFlags):
        ws=f'{self.host}{id}'
        result = {
            "parse": 1,  # <--- 必须改成 1，开启嗅探模式
            "playUrl": "",
            "url":ws ,  # 传入网页地址，让 FongMi 的浏览器去加载
            "header":self.header
        }
        return result
