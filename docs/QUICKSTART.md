# 快速开始指南

## 🚀 5分钟快速上手

### 1. 安装项目
```bash
# 克隆项目
git clone https://github.com/rojarifiroj/social-auto-upload.git
cd social-auto-upload

# 安装依赖
pip install -r requirements.txt
playwright install chromium firefox
```

### 2. 初始化项目
```bash
# 运行初始化脚本
python scripts/init_project.py
```

### 3. 配置项目
```bash
# 编辑配置文件
cp config/config.example.yaml config/config.yaml
# 使用你喜欢的编辑器编辑 config/config.yaml
```

### 4. 设置浏览器路径
在 `config/config.yaml` 中设置你的Chrome浏览器路径：

**Windows:**
```yaml
browser:
  chrome_path: "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

**macOS:**
```yaml
browser:
  chrome_path_mac: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

**Linux:**
```yaml
browser:
  chrome_path_linux: "/usr/bin/google-chrome"
```

### 5. 获取Cookie（以抖音为例）
```bash
# 运行Cookie获取脚本
python get_douyin_cookie.py
# 扫码登录，Cookie会自动保存
```

### 6. 准备视频文件
1. 将视频文件放入 `videos/` 目录
2. 为每个视频创建对应的标题文件（同名.txt文件）
3. 编辑标题文件，添加标题和话题标签

### 7. 开始上传
```bash
# 使用CLI工具上传
python cli_main.py douyin test upload "videos/your_video.mp4" -pt 0
```

## 📋 详细步骤说明

### 获取各平台Cookie

#### 抖音
```bash
python get_douyin_cookie.py
```

#### 视频号
```bash
python get_tencent_cookie.py
```

#### Bilibili
```bash
biliup.exe -u cookies/bilibili_uploader/account.json login
```

#### 小红书
1. 安装Chrome插件：EditThisCookie
2. 登录小红书网页版
3. 使用插件导出Cookie
4. 粘贴到 `uploader/xhs_uploader/accounts.ini`

#### TikTok
```bash
python get_tk_cookie.py
```

#### 快手
```bash
python examples/get_kuaishou_cookie.py
```

### 视频文件格式

#### 文件结构
```
videos/
├── video1.mp4
├── video1.txt
├── video2.mp4
└── video2.txt
```

#### 标题文件格式
```
这是视频标题 🎬
#话题标签 #短视频 #推荐

另一个标题示例
#热门 #搞笑 #生活
```

### CLI命令示例

#### 登录
```bash
# 抖音登录
python cli_main.py douyin test login

# 视频号登录
python cli_main.py tencent test login
```

#### 立即上传
```bash
# 抖音立即上传
python cli_main.py douyin test upload "videos/video.mp4" -pt 0

# 视频号立即上传
python cli_main.py tencent test upload "videos/video.mp4" -pt 0
```

#### 定时上传
```bash
# 抖音定时上传（明天12点）
python cli_main.py douyin test upload "videos/video.mp4" -pt 1 -t "2024-01-15 12:00"

# 视频号定时上传（明天18点）
python cli_main.py tencent test upload "videos/video.mp4" -pt 1 -t "2024-01-15 18:00"
```

## ⚙️ 配置说明

### 主要配置项

#### 浏览器配置
```yaml
browser:
  chrome_path: "浏览器路径"
  args: ["--no-sandbox", "--disable-dev-shm-usage"]
```

#### 上传配置
```yaml
upload:
  default_publish_type: 0  # 0=立即发布，1=定时发布
  default_daily_times: [6, 11, 14, 16, 22]  # 默认发布时间
  max_uploads_per_day: 5  # 每日最大上传数量
```

#### 平台配置
```yaml
platforms:
  douyin:
    enabled: true
    cookie_file: "cookies/douyin_uploader/account.json"
    title_file: "douyin_title_p.txt"
    settings:
      auto_cover: true
      auto_hashtag: true
```

### 环境变量

支持通过环境变量覆盖配置：

```bash
# 设置Chrome路径
export SAU_BROWSER_CHROME_PATH="/path/to/chrome"

# 启用抖音平台
export SAU_PLATFORMS_DOUYIN_ENABLED="true"

# 设置默认发布类型
export SAU_UPLOAD_DEFAULT_PUBLISH_TYPE="1"
```

## 🔧 常见问题

### Q: Chrome浏览器路径找不到？
A: 根据你的操作系统设置正确的路径：
- Windows: `C:/Program Files/Google/Chrome/Application/chrome.exe`
- macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Linux: `/usr/bin/google-chrome`

### Q: Cookie获取失败？
A: 确保：
1. 网络连接正常
2. 浏览器路径正确
3. 按照提示扫码登录
4. 等待登录完成后再关闭浏览器

### Q: 上传失败？
A: 检查：
1. Cookie是否有效
2. 视频文件是否存在
3. 标题文件格式是否正确
4. 网络连接是否稳定

### Q: 如何批量上传？
A: 可以使用脚本批量处理：
```python
import os
from pathlib import Path

videos_dir = Path("videos")
for video_file in videos_dir.glob("*.mp4"):
    # 检查是否有对应的标题文件
    title_file = video_file.with_suffix('.txt')
    if title_file.exists():
        # 执行上传命令
        os.system(f'python cli_main.py douyin test upload "{video_file}" -pt 0')
```

## 📞 获取帮助

- 📖 查看完整文档：[README.MD](README.MD)
- 🐛 报告问题：[Issues](https://github.com/rojarifiroj/social-auto-upload/issues)
- 💬 讨论交流：[Discussions](https://github.com/rojarifiroj/social-auto-upload/discussions)

## ⚠️ 注意事项

1. 请遵守各平台的使用条款
2. 不要过度频繁上传，避免账号被封
3. 定期检查Cookie有效性
4. 备份重要的配置和Cookie文件
5. 本项目仅供学习和研究使用 