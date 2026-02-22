import os
import shutil

# ================= 配置区域 =================
# 1. 串烧文件夹路径
CHUAAN_SHAO_DIR = r'D:\music\cs'

# 2. 单曲文件夹路径
DAN_QU_DIR = r'D:\music\dq'

# 3. U盘目标路径
USB_DIR = r'F:\车载'

# 4. 限制最大歌曲数量
MAX_SONGS = 150
# ===========================================

# 尝试导入 mutagen 用于精准检测音频损坏 (需: pip install mutagen)
try:
    import mutagen

    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False
    print("-" * 50)
    print("【提示】未检测到 mutagen 库，目前仅根据文件大小(>1KB)判断文件是否损坏。")
    print("建议在命令行运行: pip install mutagen 以启用精准检测功能。")
    print("-" * 50)


def is_file_corrupted(filepath):
    """
    检测文件是否损坏
    :return: True (已损坏/不可播放), False (正常)
    """
    # 1. 基础检测：文件是否存在或大小是否为0/极小
    if not os.path.exists(filepath):
        return True

    try:
        if os.path.getsize(filepath) < 1024:  # 小于1KB通常不是有效歌曲
            return True
    except OSError:
        return True

    # 2. 高级检测：使用 mutagen 读取音频头信息
    if HAS_MUTAGEN:
        try:
            # 尝试解析音频文件，如果抛出异常或返回 None 则视为损坏
            audio = mutagen.File(filepath)
            if audio is None:
                return True
        except Exception:
            return True

    return False


def remove_unplayable_files():
    """扫描U盘目录并删除无法播放的文件"""
    print(f"\n>>> 开始扫描 U 盘损坏文件: {USB_DIR}")
    if not os.path.exists(USB_DIR):
        print("U盘目录不存在，跳过扫描。")
        return

    files = [f for f in os.listdir(USB_DIR) if f.lower().endswith(('.mp3', '.flac', '.wav'))]
    deleted_count = 0

    for file_name in files:
        file_path = os.path.join(USB_DIR, file_name)

        if is_file_corrupted(file_path):
            try:
                os.remove(file_path)
                print(f"[删除损坏文件] {file_name}")
                deleted_count += 1
            except Exception as e:
                print(f"[删除失败] {file_name}: {e}")

    if deleted_count == 0:
        print("扫描完成，未发现损坏文件。")
    else:
        print(f"扫描完成，共删除 {deleted_count} 个无法播放的文件。")


def smart_move():
    # 如果U盘目标文件夹不存在则创建
    if not os.path.exists(USB_DIR):
        os.makedirs(USB_DIR)
        print(f"创建目标文件夹: {USB_DIR}")

    # 获取两个文件夹下的所有音乐文件列表
    chuan_shao_files = sorted([f for f in os.listdir(CHUAAN_SHAO_DIR) if f.lower().endswith(('.mp3', '.flac', '.wav'))])
    dan_qu_files = sorted([f for f in os.listdir(DAN_QU_DIR) if f.lower().endswith(('.mp3', '.flac', '.wav'))])

    print(f"源目录找到串烧: {len(chuan_shao_files)} 首")
    print(f"源目录找到单曲: {len(dan_qu_files)} 首")
    print(f"目标限制: {MAX_SONGS} 首")
    print("-" * 30)

    c_idx = 0
    d_idx = 0
    total_count = 0

    # 循环移动
    while (c_idx < len(chuan_shao_files) or d_idx < len(dan_qu_files)):

        # --- 步骤1: 尝试移动 2 个串烧 ---
        for _ in range(2):
            if total_count >= MAX_SONGS:
                print(f"\n已达到设定上限 ({MAX_SONGS} 首)，停止移动。")
                return

            if c_idx < len(chuan_shao_files):
                file_name = chuan_shao_files[c_idx]
                src = os.path.join(CHUAAN_SHAO_DIR, file_name)
                # 目标文件名：000_文件名.mp3
                dst_name = f"{total_count:03d}_{file_name}"
                dst = os.path.join(USB_DIR, dst_name)

                if os.path.exists(dst):
                    print(f"[跳过] U盘已存在: {dst_name}")
                else:
                    print(f"正在移动串烧 ({total_count + 1}/{MAX_SONGS}): {file_name}")
                    # 【核心修改】：使用 move 代替 copy2
                    shutil.move(src, dst)

                c_idx += 1
                total_count += 1

        # --- 步骤2: 尝试移动 1 个单曲 ---
        if total_count >= MAX_SONGS:
            print(f"\n已达到设定上限 ({MAX_SONGS} 首)，停止移动。")
            return

        if d_idx < len(dan_qu_files):
            file_name = dan_qu_files[d_idx]
            src = os.path.join(DAN_QU_DIR, file_name)
            dst_name = f"{total_count:03d}_{file_name}"
            dst = os.path.join(USB_DIR, dst_name)

            if os.path.exists(dst):
                print(f"[跳过] U盘已存在: {dst_name}")
            else:
                print(f"正在移动单曲 ({total_count + 1}/{MAX_SONGS}): {file_name}")
                # 【核心修改】：使用 move 代替 copy2
                shutil.move(src, dst)

            d_idx += 1
            total_count += 1

    print("\n移动任务完成！")
    print(f"共处理歌曲: {total_count} 首")


if __name__ == "__main__":
    # 1. 执行移动逻辑
    smart_move()

    # 2. 执行坏文件清理逻辑
    remove_unplayable_files()