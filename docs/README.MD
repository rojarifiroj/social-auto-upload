# social-auto-upload (Enhanced Version)

> **This project is a customized and enhanced version based on [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload).**
>
> In addition to all the original features, it adds:
> - **Video cutting**: Automatically or manually cut video clips for platform requirements.
> - **Add background music**: Easily add background music to your videos.
> - **Batch video processing**: Process multiple videos in one go, including cutting, music, watermark, and cover generation.
> - **Watermark and cover image tools**: Batch add watermarks and generate covers for videos and images.
> - **Internationalization**: All code comments, prompts, and documentation are in English.
> - **Improved configuration and scripts**: YAML-based config, and includes cleanup, initialization, and config migration scripts for easier maintenance.
> - **One-click maintenance scripts**: Scripts for project cleanup, initialization, and configuration migration.
> - **Better error handling and logging**: More robust for automation and batch scenarios.

---

## ✨ Enhanced Features

- **Video Cutting**: Supports automatic/manual video segment cutting to fit different platform requirements.  
  (See `tools/video_processing/cutvideo.py`)
- **Background Music**: Automatically add background music to videos, with support for custom or random tracks.  
  (See `tools/video_processing/videomaker.py`)
- **Batch Video Processing**: Process and upload multiple videos in one go, including cutting, music, watermark, and cover generation.
- **Watermark and Cover Tools**: Batch add watermarks (`watermark.py`) and download/generate covers (`picdownload.py`).
- **Internationalization**: All documentation, code comments, and prompts are in English for global collaboration.
- **YAML-based Configuration**: Unified, easy-to-edit config files, supporting environment variable overrides.
- **Project Maintenance Scripts**: Includes scripts for cleanup, initialization, and config migration (`scripts/` directory).
- **Improved Usability**: More robust error handling, logging, and batch operation support.

---

## 🆚 Difference from Upstream

This repository is forked and enhanced from [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload).

**Main differences:**
- Video cutting and background music features for short video platforms.
- Batch processing tools for video, watermark, and cover image.
- All code, documentation, and prompts are in English.
- YAML-based configuration and environment variable support.
- One-click scripts for project cleanup, initialization, and config migration.
- More robust error handling and logging for automation.
- More suitable for international developers and team collaboration.

---

> For original features and usage, see [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload).  
> For enhanced features, see the [tools/video_processing/](tools/video_processing/) and [scripts/](scripts/) directories, and the examples in [docs/examples/](docs/examples/).

# social-auto-upload This project aims to automate the posting of videos to various social media platforms

<img src="media/show/tkupload.gif" alt="tiktok show" width="800"/>

## 💡Feature
- Mainstream Chinese social media platforms:
  - [x] Douyin
  - [x] Tencent Video
  - [x] bilibili
  - [x] Xiaohongshu
  - [x] Kuaishou
  - [ ] Baijiahao

- Some international social media platforms:
  - [x] tiktok
  - [ ] youtube

---
- [ ] User-friendly version (support for non-developers): Gui or Cli
- [ ] API encapsulation
  - [ ] Docker deployment
- [ ] Automated upload (schedule)
- [x] Scheduled upload (cron)
- [x] cookie management
- [ ] International platform proxy settings
- [ ] Multi-threaded upload
- [ ] slack push

## 💾Installation

### 1. Clone the project
```bash
git clone https://github.com/rojarifiroj/social-auto-upload.git
cd social-auto-upload
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium firefox
```

### 3. Configure the project
```bash
# Copy the configuration example file
cp config/config.example.yaml config/config.yaml

# Edit the configuration file
# Modify config/config.yaml according to your actual situation
```

### 4. Configure browser path
Set your Chrome browser path in `config/config.yaml`:
```yaml
browser:
  chrome_path: "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Windows
  chrome_path_mac: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # macOS
  chrome_path_linux: "/usr/bin/google-chrome"  # Linux
```

### 5. Get Cookies
Get cookies for each platform:
```bash
# Douyin
python get_douyin_cookie.py

# Tencent Video
python get_tencent_cookie.py

# Bilibili
biliup.exe -u cookies/bilibili_uploader/account.json login

# Xiaohongshu
# Use Chrome extension EditThisCookie to export cookies, paste to uploader/xhs_uploader/accounts.ini

# TikTok
python get_tk_cookie.py

# Kuaishou
python examples/get_kuaishou_cookie.py
```

For non-programmers, [Beginner Tutorial](https://juejin.cn/post/7372114027840208911)

## 🐇 About
The project for my own project extracted, my release strategy is timed release (released a day in advance), so the release part of the event are used for the next day time!

If you need to release it immediately, you can study the source code or ask me questions.

This project was extracted from my personal project. My release strategy is scheduled release (released one day in advance), so the release events are all set for the next day's time!

If you need immediate release, you can study the source code or ask me questions.

## 📁 Project Structure
```
social-auto-upload/
├── config/                 # Configuration directory
│   ├── config.yaml        # Main configuration file
│   └── config.example.yaml # Configuration example file
├── uploader/              # Platform uploaders
│   ├── douyin_uploader/   # Douyin uploader
│   ├── tencent_uploader/  # Tencent Video uploader
│   ├── bilibili_uploader/ # Bilibili uploader
│   ├── xhs_uploader/      # Xiaohongshu uploader
│   ├── tk_uploader/       # TikTok uploader
│   └── ks_uploader/       # Kuaishou uploader
├── utils/                 # Utility modules
│   ├── config_manager.py  # Configuration manager
│   ├── base_social_media.py # Base social media class
│   └── files_times.py     # File time processing
├── examples/              # Usage examples
├── cookies/               # Cookie storage directory
├── videos/                # Video files directory
├── logs/                  # Logs directory
└── media/                 # Media files
```

## ⚙️ Configuration Instructions

### Configuration file structure
The project uses YAML format configuration files, mainly including the following parts:

1. **Basic configuration** (`base`): Project basic settings and log configuration
2. **Browser configuration** (`browser`): Chrome browser path and startup parameters
3. **Video processing configuration** (`video`): Video file related settings
4. **Upload configuration** (`upload`): Upload related parameters
5. **Platform configuration** (`platforms`): Specific configuration for each platform
6. **Proxy configuration** (`proxy`): Proxy server settings
7. **Notification configuration** (`notification`): Notification function settings
8. **Development configuration** (`development`): Development debugging related settings

### Environment variable support
The project supports overriding settings in configuration files through environment variables. The environment variable format is:
```
SAU_<config_path>_<config_item>
```

For example:
- `SAU_BROWSER_CHROME_PATH`: Override browser path
- `SAU_PLATFORMS_DOUYIN_ENABLED`: Enable/disable Douyin platform
- `SAU_UPLOAD_DEFAULT_PUBLISH_TYPE`: Set default publish type

### Core module explanation

### 1. Video file preparation (video prepare)
filepath Local video directory, directory containing

- Video files
- Video meta information txt file

For example:

file：2023-08-24_16-29-52 - This brave man perseveres daily for his beloved .mp4

meta_file:2023-08-24_16-29-52 - This brave man perseveres daily for his beloved .txt

meta_file content:
```angular2html
This brave man perseveres daily for his beloved 🥺❤️‍🩹
#perseverance #love #struggle #shortvideo
```

### Usage
1. Set `LOCAL_CHROME_PATH` in the config file (Douyin, Tencent Video, TikTok may have various compatibility issues with chromium, it's recommended to set local chrome)
2. Here are 3 paths:
   - You can study the source code yourself, free, and integrate it into your own projects
   - You can refer to the usage guides for each platform below, there are various example codes in the `examples` folder
   - Use cli for simple usage (supports TikTok, Douyin, Tencent Video)

#### cli usage
```python 
python cli_main.py <platform> <account_name> <action: upload, login> [options]
```
To view detailed parameter descriptions:
```python
python cli_main.py -h
```
```python
usage: cli_main.py [-h] platform account_name action ...

Upload video to multiple social-media.

positional arguments:
  platform      Choose social-media platform: douyin tencent tiktok kuaishou
  account_name  Account name for the platform: xiaoA
  action        Choose action
    upload      upload operation
    login       login operation
    watch       watch operation

options:
  -h, --help    show this help message and exit

```
Examples
```python
python cli_main.py douyin test login
```
Douyin platform, account name is test, action is login

```python
python cli_main.py douyin test upload "C:\Users\duperdog\Videos\2023-11-07_05-27-44 - This girl is like a fairy in dreams... .mp4" -pt 0
```
Douyin platform, account name is test, action is upload, video file (requires corresponding meta file, see above), publish method (pt): 0 immediate publish

```python
python cli_main.py douyin test upload "C:\Users\superdog\Videos\2023-11-07_05-27-44 - This girl is like a fairy in dreams... .mp4" -pt 1 -t "2024-6-14 12:00"
```
Douyin platform, account name is test, action is upload, video file, publish method (pt): 1 scheduled publish, publish time (t): 2024-6-14 12:00

---

## Detailed platform instructions

### 1. Douyin
<img src="media/show/pdf3.gif" alt="douyin show" width="500"/>

Use playwright to simulate browser behavior
> Douyin frontend implementation, many css class ids are random numbers, so the project uses relative positioning for locators instead of fixed positioning
1. Prepare video directory structure
2. Cookie acquisition: get_douyin_cookie.py scan code login
3. Upload video: upload_video_to_douyin.py 



Other parts explanation:
```
douyin_setup handle parameter is True for manual cookie acquisition, False for cookie validity verification

generate_schedule_time_next_day defaults to start from the next day (this avoids accidental time selection errors)
Parameter explanation:
- total_videos number of videos to upload this time
- videos_per_day number of videos uploaded per day
- daily_times video publish times, default 6, 11, 14, 16, 22 o'clock
- start_days start from day N
```

> December 15, 2023 supplement: Using chromium may cause issues with video cover image recognition
> Solution:
> 1. Download chrome
> 2. Find chrome installation directory
> 3. Set local chrome path in conf file LOCAL_CHROME_PATH = "xxx/xxx/chrome.exe"


Reference projects:
- https://github.com/wanghaisheng/tiktoka-studio-uploader
- https://github.com/Superheroff/douyin_uplod
- https://github.com/lishang520/DouYin-Auto-Upload.git

---

### 2. Tencent Video
Use playwright to simulate browser behavior
1. Prepare video directory structure
2. Cookie acquisition: get_tencent_cookie.py scan code login
3. Upload video: upload_video_to_tencent.py 



Other parts explanation:
```
Refer to douyin_setup configuration above
```

> Tencent Video using chromium will not support video upload, you need to specify local browser yourself
> Solution:
> 1. Download chrome
> 2. Find chrome installation directory
> 3. Set local chrome path in conf file LOCAL_CHROME_PATH = "xxx/xxx/chrome.exe"

---


### 3. Xiaohongshu
This implementation uses ReaJason's [xhs](https://github.com/ReaJason/xhs), thanks again.

1. Directory structure same as above
2. Cookie acquisition, you can use chrome extension: EditThisCookie
- Set export format
![Alt text](media/20231009111131.png)
- Export
![Alt text](media/20231009111214.png)
3. Paste to uploader/xhs_uploader/accounts.ini file


#### Explanation and notes:

```
xhs signature methods are divided into two types:
- Local signature sign_local (default)
- Self-built signature service sign

Testing found that local signature has issues in actual multi-account scenarios
So if you have multi-account distribution, it's recommended to use self-built signature service (todo upload docker configuration)
```
##### Troubleshooting
If you encounter signature issues, try updating the "utils/stealth.min.js" file
https://github.com/requireCool/stealth.min.js

24.4.10 Most people's Xiaohongshu failures are due to cookie issues, please check if your cookie is like mine
![Correct cookie](media/xhs_error_cookie.png)

For xhs part, you can refer to the author: https://reajason.github.io/xhs/basic

##### todo
- Scan code login method (experiments found differences from browser acquisition, will have issues, to be studied in the future)


Reference projects:
- https://github.com/ReaJason/xhs

---

### 4. bilibili
This implementation uses biliup's [biliup-rs](https://github.com/biliup/biliup-rs), thanks again.
1. Prepare video directory structure
2. Cookie acquisition: `biliup.exe -u account.json login` choose your preferred login method
![Login method](media/get_bili_cookie.png) 
3. Upload video: upload_video_to_bilibili.py

#### Explanation and notes:

```
bilibili cookies are long-term valid (at least that's how it's been for my 2 years of operation)
For other platforms such as linux mac server operation, please study yourself
```
Reference projects:
- https://github.com/biliup/biliup-rs

---

### 5. tiktok 
Use playwright to simulate browser behavior
1. Prepare video directory structure
2. Configure local chrome path to conf file LOCAL_CHROME_PATH = "xxx/xxx/chrome.exe"
3. Cookie acquisition: get_tk_cookie.py 
![get tiktok cookie](media/tk_login.png) 
4. Upload video: upload_video_to_tiktok.py

24.7.3 update local chrome support:
- you can upload your custom thumbnail(place `png` file at the path of `videos`)

---

### 6. Kuaishou
Use playwright to simulate browser behavior
1. Prepare video directory structure
2. Cookie acquisition: examples/get_kuaishou_cookie.py scan code login
3. Upload video: examples/upload_video_to_kuaishou.py

## 🔧 Development Guide

### Adding new platform support
1. Create a new platform directory under `uploader/`
2. Implement platform-specific upload logic
3. Add platform configuration in `config/config.yaml`
4. Update default configuration in `utils/config_manager.py`

### Configuration management
The project uses a unified configuration management system, supporting:
- YAML configuration files
- Environment variable override
- Default configuration fallback
- Configuration validation

### Logging system
The project uses loguru for log management, supporting:
- Multi-level logging
- File rotation
- Structured logging

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## ⚠️ Disclaimer

This project is for learning and research purposes only. Please comply with the terms of use of each platform and relevant laws and regulations. Any consequences arising from the use of this tool are the responsibility of the user.

## 🔗 Related Links

- [Project Homepage](https://github.com/rojarifiroj/social-auto-upload)
- [Issue Feedback](https://github.com/rojarifiroj/social-auto-upload/issues)
- [Changelog](CHANGELOG.md)