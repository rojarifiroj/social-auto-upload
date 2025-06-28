import json
import random
import time
from pathlib import Path

from uploader.bilibili_uploader.main import read_cookie_json_file, extract_keys_from_json, random_emoji, \
    BilibiliUploader
from conf import BASE_DIR
from utils.constant import VideoZoneTypes
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags

# 上传记录文件路径，文件名为 bilibili_upload_record.txt
bilibili_upload_record_file = Path(__file__).parent / "bilibili_upload_record.txt"


def read_upload_record(record_file: Path):
    """读取上传记录文件，返回已经上传的视频文件名列表"""
    if record_file.exists():
        with open(record_file, 'r', encoding='utf-8') as file:
            return file.read().splitlines()  # 读取每一行文件名
    return []


def write_upload_record(record_file: Path, file_name: str):
    """将新的上传记录追加到记录文件中"""
    with open(record_file, 'a', encoding='utf-8') as file:
        file.write(file_name + '\n')


def get_random_title_from_file(title_file: Path) -> str:
    """从标题文件中随机获取一个标题"""
    if title_file.exists():
        with open(title_file, 'r', encoding='utf-8') as file:
            titles = file.readlines()
        return random.choice(titles).strip()  # 随机选择一个标题并去掉换行符
    else:
        print(f"标题文件 {title_file.name} 不存在")
        exit()


if __name__ == '__main__':
    filepath = r'Y:\sucai\sleepykitty'
    account_file = Path(BASE_DIR / "cookies" / "bilibili_uploader" / "account.json")
    if not account_file.exists():
        print(f"{account_file.name} 配置文件不存在")
        exit()

    cookie_data = read_cookie_json_file(account_file)
    cookie_data = extract_keys_from_json(cookie_data)
    print(f"cookie ok")
    tid = VideoZoneTypes.SPORTS_FOOTBALL.value  # 设置分区id
    folder_path = Path(filepath)

    # 获取所有视频文件并按创建时间排序
    files = sorted(folder_path.rglob("*.mp4"), key=lambda x: x.stat().st_ctime)

    # 从同级目录读取标题文件
    title_file_default = Path(__file__).parent / "bilibili_title.txt"
    title_file_p = Path(__file__).parent / "bilibili_title_p.txt"
    if not title_file_default.exists() or not title_file_p.exists():
        print(f"配置文件不存在")
        exit()
    # 读取上传记录
    uploaded_files = read_upload_record(bilibili_upload_record_file)

    # 设置每次上传的视频数量
    upload_count = 1  # 修改为你想要上传的数量
    uploaded_today = 0

    for file in files:
        if uploaded_today >= upload_count:
            break

        # 检查视频文件是否已经上传过
        if file.name in uploaded_files:
            print(f"视频 {file.name} 已上传过，跳过此视频。")
            continue

        # 根据文件名选择标题文件
        if file.name.endswith('p.mp4'):
            title_file = title_file_p
        else:
            title_file = title_file_default

        # 随机选择一个标题
        title = get_random_title_from_file(title_file)
        title += random_emoji()  # 加上一个随机 emoji

        # 指定你要求的标签
        tags = ["动物总动员", "可爱", "治愈", "小奶猫", "喵星人", "安静", "解压", "猫咪", "舒缓音乐", "音乐"]
        tags_str = ','.join([tag for tag in tags])

        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags_str}")

        desc = title  # 这里设置描述与标题相同
        dtime = None  # 不定时上传

        # 实例化上传器并上传
        bili_uploader = BilibiliUploader(cookie_data, file, title, desc, tid, tags, dtime)
        upload_success = bili_uploader.upload()

        if upload_success:
            # 上传成功后记录该视频文件名
            write_upload_record(bilibili_upload_record_file, file.name)
            print(f"视频 {file.name} 上传成功，已记录到上传记录。")
            uploaded_today += 1  # 增加已上传的视频数量
        else:
            print(f"视频 {file.name} 上传失败。")

        time.sleep(30)  # 上传完成后休息 30 秒