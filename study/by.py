import re
import urllib.parse

# 你的网页源代码
text = """
"url"
:"%64%30%65%31%61%65%30%37%61%33%36%61%62%33%63%30%61%35%34%33%36%38%35%63%66%66%65%34%66%62%64%30"
"""
# 正则提取：处理了可能的换行和空格
match = re.search(r'"url\s*"\s*:\s*"([^"]+)"', text, re.DOTALL)
if match:
    encoded_str = match.group(1)

    # 执行解码
    decoded_str = urllib.parse.unquote(encoded_str)

    print("解码后的 16 进制字符串：")
    print(decoded_str)
else:
    print("未匹配到 url 内容")