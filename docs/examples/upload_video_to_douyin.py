import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags


if __name__ == '__main__':
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")
    # Get video directory
    folder_path = Path(filepath)
    # Get all files in the folder
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])
    cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        thumbnail_path = file.with_suffix('.png')
        # Print video filename, title and hashtag
        print(f"Video filename: {file}")
        print(f"Title: {title}")
        print(f"Hashtag: {tags}")
        if thumbnail_path.exists():
            app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file, thumbnail_path=thumbnail_path)
        else:
            app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file)
        asyncio.run(app.main(), debug=False)