import asyncio
from pathlib import Path

from conf import BASE_DIR
from uploader.tencent_uploader.main import weixin_setup, TencentVideo
from utils.constant import TencentZoneTypes
from utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags


if __name__ == '__main__':
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "tencent_uploader" / "account.json")
    # Get video directory
    folder_path = Path(filepath)
    # Get all files in the folder
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])
    cookie_setup = asyncio.run(weixin_setup(account_file, handle=True))
    category = TencentZoneTypes.LIFESTYLE.value  # Mark as original, required otherwise not needed
    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # Print video filename, title and hashtag
        print(f"Video filename: {file}")
        print(f"Title: {title}")
        print(f"Hashtag: {tags}")
        app = TencentVideo(title, file, tags, publish_datetimes[index], account_file, category)
        asyncio.run(app.main(), debug=False)
