import hashlib
import base64
from Crypto.Cipher import AES


def get_real_url(playPageUrl, timestamp):
    # 1. 生成 AES 解密所需的 Key 和 IV
    # 逻辑：MD5(timestamp + "jo8v9s0m4p1n2l3k")
    salt = "jo8v9s0m4p1n2l3k"
    mix_str = timestamp + salt
    md5_hash = hashlib.md5(mix_str.encode('utf-8')).hexdigest()

    # 前16位作为 Key，后16位作为 IV
    key = md5_hash[:16].encode('utf-8')
    iv = md5_hash[16:32].encode('utf-8')

    # 2. 执行 AES 解密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # playPageUrl 是 Base64 编码的
    encrypted_bytes = base64.b64decode(playPageUrl)
    decrypted_data = cipher.decrypt(encrypted_bytes)

    # 3. 去除 Pkcs7 填充
    padding_len = decrypted_data[-1]
    real_url = decrypted_data[:-padding_len].decode('utf-8')

    return real_url


# --- 填入你源码里的数据 ---
playPageUrl = "9DDGsu3gBGTrtIGZyhebfGpKbRpZA1BcEyvjcZk07I9ENQPKvwebezR6E62S6F8L2DwQysL5IguUxTlU1C3yup2vj/lenovnsADqC0y5PjlZ84XaholtYy9Qc53P0fbmZm6Ozza7LBFMM+mIA8v7PV5j+sgSvqjWkwm0TMm56OR7nr9GxyHb0ApGn+0PLbua"
timestamp = "1769600980"

try:
    video_link = get_real_url(playPageUrl, timestamp)
    print("解密后的视频直链:", video_link)
except Exception as e:
    print("解密失败，请检查参数:", e)
