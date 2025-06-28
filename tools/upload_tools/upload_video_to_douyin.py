import asyncio
import json
import random
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags

UPLOAD_RECORD_FILE = Path(BASE_DIR) / "upload_record.json"
TITLE_FILE_P = Path(BASE_DIR) / "douyin_title_p.txt"
PICDONE_PATH = Path(r'Y:\sucai\picdone')


def load_uploaded_files():
    """Load the list of uploaded files"""
    if UPLOAD_RECORD_FILE.exists():
        with open(UPLOAD_RECORD_FILE, 'r') as f:
            return json.load(f)
    return []


def save_uploaded_file(file):
    """Save the uploaded filename"""
    uploaded_files = load_uploaded_files()
    uploaded_files.append(str(file))
    with open(UPLOAD_RECORD_FILE, 'w') as f:
        json.dump(uploaded_files, f)


def is_already_uploaded(file):
    """Check if the file has already been uploaded"""
    uploaded_files = load_uploaded_files()
    return str(file) in uploaded_files


def has_corresponding_txt(file):
    """Check if there is a .txt file with the same name as the video file in the same directory"""
    txt_file = file.with_suffix('.txt')
    return txt_file.exists()


def get_random_title_p():
    """Get a random title from douyin_title_p.txt"""
    if TITLE_FILE_P.exists():
        with open(TITLE_FILE_P, 'r', encoding='utf-8') as f:  # Specify utf-8 encoding
            titles = [line.strip() for line in f if line.strip()]
        if titles:
            return random.choice(titles)
    return None


def get_random_thumbnail():
    """Get a random cover image from picdone"""
    pic_files = list(PICDONE_PATH.glob("*.png"))
    if pic_files:
        return random.choice(pic_files)
    return None


if __name__ == '__main__':
    filepath = r'Y:\sucai\douyin'
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")

    # Set maximum upload count per session
    max_upload_count = 5

    # Get video directory
    folder_path = Path(filepath)
    # Use rglob to recursively get all mp4 files
    files = list(folder_path.rglob("*.mp4"))

    # Filter eligible files (not uploaded and have corresponding .txt file)
    eligible_files = [
        file for file in files
        if not is_already_uploaded(file) and ( file.stem[-1].lower() == 'p'  or (
            file.stem[-1].lower() != 'p' and has_corresponding_txt(file))
        )
    ]
    # Randomly shuffle the list of eligible files
    random.shuffle(eligible_files)

    # Control single upload count
    eligible_files = eligible_files[:max_upload_count]

    file_num = len(eligible_files)
    # publish_datetimes = generate_schedule_time_next_day(file_num, 3, daily_times=[12])
    cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))

    for index, file in enumerate(eligible_files):
        # Remove file extension
        file_stem = file.stem

        if file_stem and file_stem[-1].lower() == 'p':  # Check the last character after removing extension
            print(f"filename contains 'p'：{file.name}")
            title = get_random_title_p() or "Default Title"  # Get random title from douyin_title_p.txt
            tags = ['入眠曲', '安静的音乐', '每日吸猫', '萌宠', '失眠']
            thumbnail_path = get_random_thumbnail()  # Get random cover from Y:\sucai\picdone
            # Print video filename, title and hashtag
            print(f"Upload video filename p：{file}")
            print(f"Title p：{title}")
            print(f"Hashtag p：{tags}")
        else:
            title, tags = get_title_and_hashtags(str(file))  # Normal process to get title and hashtags
            thumbnail_path = file.with_suffix('.png')
            # Print video filename, title and hashtag
            print(f"Upload video filename：{file}")
            print(f"Title：{title}")
            print(f"Hashtag：{tags}")

        # Create video upload object
        if thumbnail_path and thumbnail_path.exists():
            app = DouYinVideo(title, file, tags, None, account_file, thumbnail_path=thumbnail_path)
        else:
            app = DouYinVideo(title, file, tags, None, account_file)

        # Upload video
        asyncio.run(app.main(), debug=False)

        # Record after successful upload
        save_uploaded_file(file)

    print("Processing completed")
