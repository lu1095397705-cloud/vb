import requests
import re
import json
import base64
from urllib.parse import unquote

# 禁用 SSL 警告
requests.packages.urllib3.disable_warnings()


def get_bttwo_m3u8(play_url):
    session = requests.Session()

    # 模拟真实的浏览器 Header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bttwo.me/',
        'Origin': 'https://www.bttwo.me'
    }

    try:
        # --- 步骤 1: 请求 BTTWO 播放页面 ---
        res1 = session.get(play_url, headers=headers, timeout=10)
        # 提取 player_aaaa
        player_data = re.search(r'var\s+player_aaaa\s*=\s*(\{.*?\})', res1.text).group(1)
        player_json = json.loads(player_data)

        # 提取并解码初始解析 URL (BTTWO 有时会 base64 加密这个 url)
        raw_url = player_json['url']
        if not raw_url.startswith('http'):
            # 如果是加密的，尝试 base64 解码
            raw_url = base64.b64decode(raw_url).decode('utf-8')

        # --- 步骤 2: 请求解析器中间页 (kvmplay.org) ---
        # 这一步是为了拿到你截图里那段 JS 源码
        headers['Referer'] = play_url
        res2 = session.get(raw_url, headers=headers, timeout=10, verify=False)
        html_source = res2.text

        # --- 步骤 3: 从 JS 源码中提取动态参数 (关键点!) ---
        # 使用正则提取你截图里看到的那些变量
        mysvg = re.search(r"const\s+mysvg\s*=\s*'(.*?)'", html_source).group(1)
        expires = re.search(r"expires:\s*'(.*?)'", html_source).group(1)
        client = re.search(r"client:\s*'(.*?)'", html_source).group(1)
        nonce = re.search(r"nonce:\s*'(.*?)'", html_source).group(1)
        token = re.search(r"token:\s*'(.*?)'", html_source).group(1)

        # --- 步骤 4: 发送 POST 请求获取 m3u8 ---
        post_headers = {
            "User-Agent": headers['User-Agent'],
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://play.kvmplay.org",
            "Referer": raw_url,  # 这一步 Referer 必须是解析页地址
            "Accept": "*/*"
        }

        payload = {
            "expires": expires,
            "client": client,
            "nonce": nonce,
            "token": token,
            "source": mysvg
        }

        # 注意：这里要发送的是 JSON 字符串
        res3 = session.post(mysvg, headers=post_headers, data=json.dumps(payload), timeout=10, verify=False)

        if res3.status_code == 200:
            data = res3.json()
            if data.get('ok'):
                return data.get('url')
            else:
                print("解析接口返回错误:", data)
        else:
            print(f"POST 请求失败, 状态码: {res3.status_code}, 响应: {res3.text}")

    except Exception as e:
        print(f"解析过程中发生错误: {e}")

    return None


# 测试运行
if __name__ == "__main__":
    # 找一个具体的 BTTWO 播放页面测试
    test_url = "https://www.bttwo.me/v_play/bXZfMTM1NDY=.html"
    final_m3u8 = get_bttwo_m3u8(test_url)
    if final_m3u8:
        print("成功获取播放地址:", final_m3u8)
    else:
        print("获取失败，请检查正则或网络。")