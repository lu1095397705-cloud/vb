import requests
import time


def get_play_url(video_id, episode_id):
    url = "https://www.ksnnhbj.com/api/mw-movie/anonymous/v2/video/episode/url"

    params = {
        "clientType": "1",
        "id": video_id,
        "nid": episode_id
    }

    headers = {
        "authorization": "__51vcke__3I14AJXLSVMADZTk=f1927215-af42-5d95-9eee-cc73b2dbbb0a; __51vuft__3I14AJXLSVMADZTk=1775051296579; UM_distinctid=19d494d5b59e4a-0956dc843cf129-26061f51-fa000-19d494d5b5ac9e; CNZZDATA1281332409=497050465-1775051300-https%253A%252F%252Fcn.bing.com%252F%7C1775054327; __vtins__3I14AJXLSVMADZTk=%7B%22sid%22%3A%20%228ad462b0-c06e-5f7c-8cec-7b3bb9155f9d%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201775058031901%2C%20%22ct%22%3A%201775056231901%7D; __51uvsct__3I14AJXLSVMADZTk=3",  # 填入你抓到的完整token
        "sign": "f2ba5daab1a354bb1888e1f0a85ed4e2630525da",  # 填入你抓到的sign
        "t": "1775056232476",  # 填入对应的t
        "client-type": "1",
        "deviceId": "e2389eb5-62bb-400f-8a98-fe36ee4d9b32",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Referer": f"https://www.ksnnhbj.com/vod/play/{video_id}/sid/{episode_id}",
        "Accept": "application/json, text/plain, */*"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(response.text)  # 打印看看结果
        return response.json()
    except Exception as e:
        print(f"请求失败: {e}")


# 测试
get_play_url("143234", "1271978")