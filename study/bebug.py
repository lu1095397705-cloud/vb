import os
import shutil
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.flac import FLAC
from mutagen.wave import WAVE

# ================= 配置区域 =================
# U盘的路径
USB_PATH = r'E:\车载'

# 是否开启“真实删除”模式？
# True = 直接删除文件（不可恢复）
# False = 只打印会删除哪些文件，不实际执行（建议第一次先填 False 测试）
REAL_DELETE = True


# ===========================================

def check_and_clean(folder_path):
    print(f"正在扫描: {folder_path} ...")

    deleted_count = 0
    error_count = 0

    # 遍历文件夹下所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()

            reason = None

            # --- 检查规则 1: 苹果系统产生的垃圾文件 (._开头) ---
            if file.startswith("._"):
                reason = "MacOS缓存垃圾文件"

            # --- 检查规则 2: 文件过小 (小于 10KB) ---
            # 正常的一首歌通常在 3MB 以上，小于 10KB 必定是损坏的或非音频
            elif os.path.getsize(file_path) < 10 * 1024:
                # 排除一下封面图片，只针对音频格式
                if file_lower.endswith(('.mp3', '.flac', '.wav', '.m4a')):
                    reason = "文件过小(损坏)"

            # --- 检查规则 3: 深度检测音频流 ---
            else:
                try:
                    if file_lower.endswith('.mp3'):
                        audio = MP3(file_path)
                        # 尝试读取时长，如果时长为0或读取报错，视为坏歌
                        if audio.info.length == 0:
                            reason = "音频时长为0"
                    elif file_lower.endswith('.flac'):
                        FLAC(file_path)
                    elif file_lower.endswith('.wav'):
                        WAVE(file_path)

                    # 如果能跑到这里，说明文件基本是健康的

                except HeaderNotFoundError:
                    reason = "文件头损坏(Header Missing)"
                except Exception as e:
                    reason = f"无法解码: {str(e)}"

            # --- 执行删除逻辑 ---
            if reason:
                print(f"[发现坏歌] {file} -> 原因: {reason}")
                error_count += 1

                if REAL_DELETE:
                    try:
                        os.remove(file_path)
                        print(f"  └─> 已删除")
                        deleted_count += 1
                    except Exception as e:
                        print(f"  └─> 删除失败 (可能被占用): {e}")
                else:
                    print(f"  └─> (模拟模式) 未执行删除")

    print("\n" + "=" * 30)
    print(f"扫描完成！")
    print(f"发现问题文件: {error_count} 个")
    if REAL_DELETE:
        print(f"成功清理文件: {deleted_count} 个")
    else:
        print("当前为模拟模式，请将代码中的 REAL_DELETE 改为 True 以执行删除。")
    print("=" * 30)


if __name__ == "__main__":
    if os.path.exists(USB_PATH):
        check_and_clean(USB_PATH)
    else:
        print(f"错误：找不到路径 {USB_PATH}，请检查U盘盘符。")