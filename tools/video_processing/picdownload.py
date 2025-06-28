import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # 引入 Service
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Pinterest 网址
url = "https://www.pinterest.com/aynulsworldbd/cute-cat-collection/"

# 保存图片的文件夹路径
output_folder = "/Volumes/Download/sucai/autopic"
os.makedirs(output_folder, exist_ok=True)

# 设置 Chrome 浏览器的驱动程序路径
chrome_driver_path = "/Users/yuyang/Downloads/chromedriver-mac-arm64/chromedriver"  # 替换为你本地的 chromedriver 路径
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无界面模式

# 使用 Service 初始化 ChromeDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 访问 Pinterest 页面
driver.get(url)

# 模拟向下滚动页面，加载更多图片
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 向下滚动到页面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 等待页面加载
    time.sleep(scroll_pause_time)

    # 计算新的页面高度并检查是否已到底部
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 获取页面源代码
page_source = driver.page_source
driver.quit()

# 解析页面内容
soup = BeautifulSoup(page_source, "html.parser")
img_tags = soup.find_all("img")

# 下载所有图片
for img_tag in img_tags:
    img_url = img_tag.get("src")

    # 跳过无效的图片链接
    if not img_url or not img_url.startswith("http"):
        continue

    # 获取图片的高清版本
    if "236x" in img_url:
        img_url = img_url.replace("236x", "originals")

    img_name = os.path.basename(img_url)

    # 下载并保存图片
    try:
        img_data = requests.get(img_url).content
        img_path = os.path.join(output_folder, img_name)

        with open(img_path, "wb") as img_file:
            img_file.write(img_data)
            print(f"图片已下载: {img_name}")
    except Exception as e:
        print(f"下载失败: {img_url} 错误信息: {e}")

print("所有图片下载完成！")
