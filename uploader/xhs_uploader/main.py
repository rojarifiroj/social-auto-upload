import configparser
import json
import pathlib
from time import sleep

import requests
from playwright.sync_api import sync_playwright

from conf import BASE_DIR, XHS_SERVER

config = configparser.RawConfigParser()
config.read('accounts.ini')


def sign_local(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = pathlib.Path(BASE_DIR / "utils/stealth.min.js")
                chromium = playwright.chromium

                # If it keeps failing, try setting to False to open browser, add sleep appropriately to check browser status
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # After setting browser cookie here, if you don't sleep a bit, signature acquisition will fail, if it fails often, try setting it longer
                sleep(2)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # Sometimes "window._webmsxyw is not a function" or unknown redirect errors occur here, so add failure retry
            pass
    raise Exception("Tried so many times but still can't get signature successfully, giving up")


def sign(uri, data=None, a1="", web_session=""):
    # Fill in your own flask signature service port address
    res = requests.post(f"{XHS_SERVER}/sign",
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }


def beauty_print(data: dict):
    print(json.dumps(data, ensure_ascii=False, indent=2))
