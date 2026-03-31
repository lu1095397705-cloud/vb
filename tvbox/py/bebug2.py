import urllib.parse
# 原始编码字符串
encoded_str = "%59%59%4E%42%2D%39%36%35%63%34%33%39%65%62%62%61%64%31%63%35%66%38%63%33%32%35%65%65%66%62%30%31%31%66%61%34%30"
# 使用 unquote 进行解码
decoded_str = urllib.parse.unquote(encoded_str)
print(decoded_str)