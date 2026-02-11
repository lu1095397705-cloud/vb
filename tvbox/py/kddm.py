
import requests
from bs4 import BeautifulSoup
from base.spider import Spider
import random
import time
import  sys

class Spider(Spider):
    def init(self, extend=""):
        self.host = "https://cn.xgcartoon.com/"
        self.header = {
            'User-Agent':'com.android.chrome/131.0.6778.200 (Linux;Android 9) AndroidXMedia3/1.8.0',
            'Referer': f'{self.host}'

        }



    def homeContent(self, filter):
        result={}
        result['class'] = [
            {"type_id": "cn", "type_name": "国漫"}
        ]
        return result



    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        time.sleep(random.uniform(2, 4))
        url=f'{self.host}/classify?type=%2a&region={tid}&state=%2a&filter=%2a'
        res=self.fetch(url,headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        video=[]
        result={}
        for li in soup.find_all('div', class_='col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-6 topic-list-box'):
            vod_id = li.find('a').get('href')
            vod_name = li.find('div', class_='h3 mb12').get_text(strip=True)
            vod_pic = li.find('amp-img').get('src')
            data-origina
    def detailContent(self, ids):
        time.sleep(random.uniform(3, 5))
        vid=ids[0]
        url=f'{self.host}{vid}'
        res=self.fetch(url,headers=self.header)
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
        time.sleep(random.uniform(5, 8))
        url=f'https://cn.xgcartoon.com/search?q={key}'
        res=self.fetch(url,hesders=self.header)
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
            "header":self.header,
            "timeout":35
        }
        return result
