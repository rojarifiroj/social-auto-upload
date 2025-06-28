# -*- coding: utf-8 -*-
from datetime import datetime

from playwright.async_api import Playwright, async_playwright
import os
import asyncio

from conf import LOCAL_CHROME_PATH
from utils.base_social_media import set_init_script
from utils.files_times import get_absolute_path
from utils.log import tencent_logger


def format_str_for_short_title(origin_title: str) -> str:
    # Define allowed special characters
    allowed_special_chars = "《》"":+?%°"

    # Remove disallowed special characters
    filtered_chars = [char if char.isalnum() or char in allowed_special_chars else ' ' if char == ',' else '' for
                      char in origin_title]
    formatted_string = ''.join(filtered_chars)

    # Adjust string length
    if len(formatted_string) > 16:
        # Truncate string
        formatted_string = formatted_string[:16]
    elif len(formatted_string) < 6:
        # Use spaces to pad string
        formatted_string += ' ' * (6 - len(formatted_string))

    return formatted_string


async def cookie_auth(account_file):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=account_file)
        context = await set_init_script(context)
        # Create a new page
        page = await context.new_page()
        # Visit the specified URL
        await page.goto("https://channels.weixin.qq.com/platform/post/create")
        try:
            await page.wait_for_selector('div.title-name:has-text("微信小店")', timeout=5000)  # Wait 5 seconds
            tencent_logger.error("[+] Wait 5 seconds, cookie expired")
            return False
        except:
            tencent_logger.success("[+] Cookie is valid")
            return True


async def get_tencent_cookie(account_file):
    async with async_playwright() as playwright:
        options = {
            'args': [
                '--lang en-GB'
            ],
            'headless': False,  # Set headless option here
        }
        # Make sure to run headed.
        browser = await playwright.chromium.launch(**options)
        # Setup context however you like.
        context = await browser.new_context()  # Pass any options
        # Pause the page, and start recording manually.
        context = await set_init_script(context)
        page = await context.new_page()
        await page.goto("https://channels.weixin.qq.com")
        await page.pause()
        # Click continue in debugger, save cookie
        await context.storage_state(path=account_file)


async def weixin_setup(account_file, handle=False):
    account_file = get_absolute_path(account_file, "tencent_uploader")
    if not os.path.exists(account_file) or not await cookie_auth(account_file):
        if not handle:
            # Todo alert message
            return False
        tencent_logger.info('[+] Cookie file does not exist or has expired, browser will open automatically, please scan code to login, cookie file will be generated automatically after login')
        await get_tencent_cookie(account_file)
    return True


class TencentVideo(object):
    def __init__(self, title, file_path, tags, publish_date: datetime, account_file, category=None):
        self.title = title  # Video title
        self.file_path = file_path
        self.tags = tags
        self.publish_date = publish_date
        self.account_file = account_file
        self.category = category
        self.local_executable_path = LOCAL_CHROME_PATH

    async def set_schedule_time_tencent(self, page, publish_date):
        label_element = page.locator("label").filter(has_text="定时").nth(1)
        await label_element.click()

        await page.click('input[placeholder="请选择发表时间"]')

        str_month = str(publish_date.month) if publish_date.month > 9 else "0" + str(publish_date.month)
        current_month = str_month + "月"
        # Get current month
        page_month = await page.inner_text('span.weui-desktop-picker__panel__label:has-text("月")')

        # Check if current month matches target month
        if page_month != current_month:
            await page.click('button.weui-desktop-btn__icon__right')

        # Get page elements
        elements = await page.query_selector_all('table.weui-desktop-picker__table a')

        # Iterate through elements and click matching element
        for element in elements:
            if 'weui-desktop-picker__disabled' in await element.evaluate('el => el.className'):
                continue
            text = await element.inner_text()
            if text.strip() == str(publish_date.day):
                await element.click()
                break

        # Input hour part (assume selecting 11 hour)
        await page.click('input[placeholder="请选择时间"]')
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.type(str(publish_date.hour))

        # Select title bar (make scheduled time effective)
        await page.locator("div.input-editor").click()

    async def handle_upload_error(self, page):
        tencent_logger.info("Video error occurred, re-uploading")
        await page.locator('div.media-status-content div.tag-inner:has-text("删除")').click()
        await page.get_by_role('button', name="删除", exact=True).click()
        file_input = page.locator('input[type="file"]')
        await file_input.set_input_files(self.file_path)

    async def upload(self, playwright: Playwright) -> None:
        # Use Chromium (here using system browser, using chromium will cause h264 error
        browser = await playwright.chromium.launch(headless=False, executable_path=self.local_executable_path)
        # Create a browser context using the specified cookie file
        context = await browser.new_context(storage_state=f"{self.account_file}")
        context = await set_init_script(context)

        # Create a new page
        page = await context.new_page()
        # Visit the specified URL
        await page.goto("https://channels.weixin.qq.com/platform/post/create")
        tencent_logger.info(f'[+]Uploading-------{self.title}.mp4')
        # Wait for page to navigate to specified URL, if not entered, automatically wait until timeout
        await page.wait_for_url("https://channels.weixin.qq.com/platform/post/create")
        # await page.wait_for_selector('input[type="file"]', timeout=10000)
        file_input = page.locator('input[type="file"]')
        await file_input.set_input_files(self.file_path)
        # Fill title and topics
        await self.add_title_tags(page)
        # Add products
        # await self.add_product(page)
        # Collection feature
        await self.add_collection(page)
        # Original selection
        await self.add_original(page)
        # Detect upload status
        await self.detect_upload_status(page)
        if self.publish_date != 0:
            await self.set_schedule_time_tencent(page, self.publish_date)
        # Add short title
        await self.add_short_title(page)

        await self.click_publish(page)

        await context.storage_state(path=f"{self.account_file}")  # Save cookie
        tencent_logger.success('  [-]Cookie update completed!')
        await asyncio.sleep(2)  # Delay here for easy visual observation
        # Close browser context and browser instance
        await context.close()
        await browser.close()

    async def add_short_title(self, page):
        short_title_element = page.get_by_text("短标题", exact=True).locator("..").locator(
            "xpath=following-sibling::div").locator(
            'span input[type="text"]')
        if await short_title_element.count():
            short_title = format_str_for_short_title(self.title)
            await short_title_element.fill(short_title)

    async def click_publish(self, page):
        while True:
            try:
                publish_buttion = page.locator('div.form-btns button:has-text("发表")')
                if await publish_buttion.count():
                    await publish_buttion.click()
                await page.wait_for_url("https://channels.weixin.qq.com/platform/post/list", timeout=1500)
                tencent_logger.success("  [-]Video published successfully")
                break
            except Exception as e:
                current_url = page.url
                if "https://channels.weixin.qq.com/platform/post/list" in current_url:
                    tencent_logger.success("  [-]Video published successfully")
                    break
                else:
                    tencent_logger.exception(f"  [-] Exception: {e}")

    async def detect_upload_status(self, page):
        while True:
            # Match delete button, represent video upload completed, if not exist, represent video is uploading, wait
            try:
                # Match delete button, represent video upload completed
                if "weui-desktop-btn_disabled" not in await page.get_by_role("button", name="发表").get_attribute(
                        'class'):
                    tencent_logger.info("  [-]Video upload completed")
                    break
                else:
                    tencent_logger.info("  [-]  Video is uploading...")
                    await asyncio.sleep(2)
                    # Video error
                    if await page.locator('div.status-msg.error').count() and await page.locator(
                            'div.media-status-content div.tag-inner:has-text("删除")').count():
                        tencent_logger.error("  [-]  Found upload error...prepare to retry")
                        await self.handle_upload_error(page)
            except:
                tencent_logger.info("  [-]  Video is uploading...")
                await asyncio.sleep(2)

    async def add_title_tags(self, page):
        await page.locator("div.input-editor").click()
        await page.keyboard.type(self.title)
        await page.keyboard.press("Enter")
        for index, tag in enumerate(self.tags, start=1):
            await page.keyboard.type("#" + tag)
            await page.keyboard.press("Space")
        tencent_logger.info(f"Successfully added hashtag: {len(self.tags)}")

    async def add_collection(self, page):
        collection_elements = page.get_by_text("添加到合集").locator("xpath=following-sibling::div").locator(
            '.option-list-wrap > div')
        if await collection_elements.count() > 1:
            await page.get_by_text("添加到合集").locator("xpath=following-sibling::div").click()
            await collection_elements.first.click()

    async def add_original(self, page):
        if await page.get_by_label("视频为原创").count():
            await page.get_by_label("视频为原创").check()
        # Check "I have read and agree to the Video Number Original Declaration Usage Terms" element whether exist
        label_locator = await page.locator('label:has-text("我已阅读并同意 《视频号原创声明使用条款》")').is_visible()
        if label_locator:
            await page.get_by_label("我已阅读并同意 《视频号原创声明使用条款》").check()
            await page.get_by_role("button", name="声明原创").click()
        # 2023年11月20日 wechat更新: 可能新账号或者改版账号，出现新的选择页面
        if await page.locator('div.label span:has-text("声明原创")').count() and self.category:
            # Because of punishment cannot select original, so first judge whether available
            if not await page.locator('div.declare-original-checkbox input.ant-checkbox-input').is_disabled():
                await page.locator('div.declare-original-checkbox input.ant-checkbox-input').click()
                if not await page.locator(
                        'div.declare-original-dialog label.ant-checkbox-wrapper.ant-checkbox-wrapper-checked:visible').count():
                    await page.locator('div.declare-original-dialog input.ant-checkbox-input:visible').click()
            if await page.locator('div.original-type-form > div.form-label:has-text("原创类型"):visible').count():
                await page.locator('div.form-content:visible').click()  # Pull down menu
                await page.locator(
                    f'div.form-content:visible ul.weui-desktop-dropdown__list li.weui-desktop-dropdown__list-ele:has-text("{self.category}")').first.click()
                await page.wait_for_timeout(1000)
            if await page.locator('button:has-text("声明原创"):visible').count():
                await page.locator('button:has-text("声明原创"):visible').click()

    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)
