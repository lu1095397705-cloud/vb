import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
headers = {
    'user-agent':'Mozilla/5.0 (Linux; Android 13; PGEM10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'referer':'https://jciyuan.com/',
    'cookie':'HWTOKEN=cecf5e608cec99abe905e4715e5ea9c03ee4fa20e7954e14702fd83dce66ed2d; HWIDHASH=936f29746732961da43766a0f1c368fc; mx_style=black; showBtn=true; PHPSESSID=bhg28fus5hhm5t3ggshaqli518; user_id=34574; user_name=cn6666; group_id=2; group_name=%E9%BB%98%E8%AE%A4%E4%BC%9A%E5%91%98; user_check=bc7c259a922f2df0ec570b76060597c1; user_portrait=%2Fstatic%2Fimages%2Ftouxiang.png; mac_history_mxpro=%5B%7B%22vod_name%22%3A%22%E4%BB%99%E9%80%86%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F55-4-1.html%22%2C%22vod_part%22%3A%221%22%7D%2C%7B%22vod_name%22%3A%22%E5%90%9E%E5%99%AC%E6%98%9F%E7%A9%BA%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F32-4-97.html%22%2C%22vod_part%22%3A%2297%22%7D%2C%7B%22vod_name%22%3A%22%E6%AD%A6%E7%A5%9E%E4%B8%BB%E5%AE%B0%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F20-6-1.html%22%2C%22vod_part%22%3A%221%22%7D%2C%7B%22vod_name%22%3A%22%E9%80%86%E5%A4%A9%E8%87%B3%E5%B0%8A%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F42-3-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%2C%7B%22vod_name%22%3A%22%E4%B9%9D%E9%98%B3%E6%AD%A6%E7%A5%9E%22%2C%22vod_url%22%3A%22https%3A%2F%2Fjciyuan.com%2Facgplay%2F36775-4-1.html%22%2C%22vod_part%22%3A%221%22%7D%5D'

}
url='https://jciyuan.com/acgplay/55-4-3.html'
response =requests.get(url, headers=headers,timeout=10)
html_content = response.text
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
play_url='https://bfq.lggys.com/player?url='+final_url









