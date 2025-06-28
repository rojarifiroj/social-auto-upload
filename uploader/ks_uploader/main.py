# -*- coding: utf-8 -*-
from datetime import datetime

from playwright.async_api import Playwright, async_playwright
import os
import asyncio

from utils.base_social_media import set_init_script
from utils.files_times import get_absolute_path
from utils.log import kuaishou_logger


async def cookie_auth(account_file):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=account_file)
        context = await set_init_script(context)
        # Create a new page
        page = await context.new_page()
        # Visit the specified URL
        await page.goto("https://cp.kuaishou.com/article/publish/video")
        try:
            await page.wait_for_selector("div.names div.container div.name:text('机构服务')", timeout=5000)  # Wait 5 seconds

            kuaishou_logger.info("[+] Waiting 5 seconds, cookie expired")
            return False
        except:
            kuaishou_logger.success("[+] Cookie valid")
            return True


async def ks_setup(account_file, handle=False):
    account_file = get_absolute_path(account_file, "ks_uploader")
    if not os.path.exists(account_file) or not await cookie_auth(account_file):
        if not handle:
            return False
        kuaishou_logger.info('[+] Cookie file does not exist or has expired, browser will open automatically, please scan QR code to login, cookie file will be generated automatically after login')
        await get_ks_cookie(account_file)
    return True


async def get_ks_cookie(account_file):
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
        context = await set_init_script(context)
        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.goto("https://cp.kuaishou.com")
        await page.pause()
        # Click continue in debugger, save cookie
        await context.storage_state(path=account_file)


class KSVideo(object):
    def __init__(self, title, file_path, tags, publish_date: datetime, account_file):
        self.title = title  # Video title
        self.file_path = file_path
        self.tags = tags
        self.publish_date = publish_date
        self.account_file = account_file
        self.date_format = '%Y-%m-%d %H:%M'

    async def handle_upload_error(self, page):
        kuaishou_logger.error("Video error occurred, re-uploading")
        await page.locator('div.progress-div [class^="upload-btn-input"]').set_input_files(self.file_path)

    async def upload(self, playwright: Playwright) -> None:
        # Launch a browser instance using Chromium browser
        browser = await playwright.chromium.launch(headless=False)
        # Create a browser context using the specified cookie file
        context = await browser.new_context(storage_state=f"{self.account_file}")
        context = await set_init_script(context)

        # Create a new page
        page = await context.new_page()
        # Visit the specified URL
        await page.goto("https://cp.kuaishou.com/article/publish/video")
        kuaishou_logger.info('Uploading-------{}.mp4'.format(self.title))
        # Wait for page to navigate to specified URL, if not entered, automatically wait until timeout
        kuaishou_logger.info('Opening main page...')
        await page.wait_for_url("https://cp.kuaishou.com/article/publish/video")
        # Click "Upload Video" button
        await page.locator("div.vVExjn9O3UQ- input").set_input_files(self.file_path)

        await asyncio.sleep(2)

        if not await page.get_by_text("封面编辑").count():
            raise Exception("Seems like didn't navigate to edit page")

        await asyncio.sleep(1)

        # Wait for button to be interactive
        new_feature_button = page.locator('button[type="button"] span:text("我知道了")')
        if await new_feature_button.count() > 0:
            await new_feature_button.click()

        kuaishou_logger.info("Filling title and topics...")
        await page.get_by_text('填写描述').locator("xpath=following-sibling::div").click()
        kuaishou_logger.info("clear existing title")
        await page.keyboard.press("Backspace")
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.press("Delete")
        kuaishou_logger.info("filling new  title")
        await page.keyboard.type(self.title)
        await page.keyboard.press("Enter")

        # Kuaishou can only add 3 topics
        for index, tag in enumerate(self.tags[:3], start=1):
            kuaishou_logger.info("Adding topic %s" % index)
            await page.locator('span:text("#话题")').click()
            await page.type('div.clGhv3UpdEo-', tag, delay=100)
            await asyncio.sleep(2)
            await page.locator('div.FZcv90s7kFs- > div').nth(0).click()

        while True:
            try:
                number = await page.locator('div > span:text("上传成功")').count()
                if number > 0:
                    kuaishou_logger.success("Video upload completed")
                    break
                else:
                    kuaishou_logger.info("Uploading video...")
                    await asyncio.sleep(2)
            except:
                kuaishou_logger.info("Uploading video...")
                await asyncio.sleep(2)

        # Scheduled task
        if self.publish_date != 0:
            await self.set_schedule_time(page, self.publish_date)

        # Check if video was published successfully
        while True:
            # Check if video was published successfully
            try:
                publish_button = page.get_by_role('button', name="发布", exact=True)
                if await publish_button.count():
                    await publish_button.click()

                await asyncio.sleep(1)
                confirm_button = page.locator("button > span:text('确认发布')")
                if await confirm_button.count():
                    await page.locator("button > span:text('确认发布')").click()

                await page.wait_for_url("https://cp.kuaishou.com/article/manage/video?status=2&from=publish",
                                        timeout=1500)
                kuaishou_logger.success("Video published successfully")
                break
            except:
                kuaishou_logger.info("Publishing video...")
                await page.screenshot(full_page=True)
                await asyncio.sleep(0.5)

        await context.storage_state(path=self.account_file)  # Save cookie
        kuaishou_logger.info('Cookie update completed!')
        await asyncio.sleep(2)  # This delay is for easy visual observation
        # Close browser context and browser instance
        await context.close()
        await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)

    async def set_schedule_time(self, page, publish_date):
        kuaishou_logger.info("click schedule")
        publish_date_hour = publish_date.strftime("%Y-%m-%d %H:%M:%S")
        await page.locator("label:text('发布时间')").locator('xpath=following-sibling::div').locator(
            '.ant-radio-input').nth(1).click()
        await asyncio.sleep(1)

        await page.locator('div.ant-picker-input input[placeholder="选择日期时间"]').click()
        await asyncio.sleep(1)

        await page.keyboard.press("Control+KeyA")
        await page.keyboard.type(str(publish_date_hour))
        await page.keyboard.press("Enter")
        await asyncio.sleep(1)


