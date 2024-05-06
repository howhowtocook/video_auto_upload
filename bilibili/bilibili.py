import os
import json
import time
import emoji
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

print("start to upload to bilibili")

def bl_browser_initial():
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.bilibili.com/')
        time.sleep(10) 
        print("Browser initialized successfully.")
        return browser
    except Exception as e:
        print("An error occurred in bl_browser_initial:", str(e))
        return None
 
def bl_log(browser):
    try:
        with open('bilibili/bilibili_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        for cookie in listCookies:
            cookie_dict = {
                'domain': '.bilibili.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            browser.add_cookie(cookie_dict)
        time.sleep(1) 
        browser.refresh()                      # Refresh the webpage to apply cookies
        time.sleep(10) 
        print("Logged in successfully.")
    except Exception as e:
        print("An error occurred in bl_log:", str(e))

def remove_special_characters(title):
    title_without_last_item = title[:title.rfind('[')].strip()
    title_without_emoji = emoji.demojize(title_without_last_item)
    return title_without_emoji
    
def bl_input_file(browser, file_path):
    try:
        time.sleep(10)
        search = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
        search.send_keys(file_path)

        time.sleep(10)

        # Find the close button inside the bcc-dialog
        close_button = browser.find_element(By.CSS_SELECTOR, ".bcc-dialog__header .bcc-dialog__close")

        # Click the close button to close the dialog
        close_button.click()

        while "上传完成" != browser.find_element(By.CSS_SELECTOR, "#video-up-app > div.content > div > div > div.video-basic > div.video-file > div.file-block > div.file-block-detail > div.file-block-status > div.file-block-status-text > span").get_attribute("innerHTML"):
            time.sleep(3)
        
        print("Video uploaded successfully.")
    except TimeoutException:
        print("Timeout: Unable to locate the file input element.")
    except Exception as e:
        print("An error occurred in bl_input_file:", str(e))

def bl_add_description(browser,file_path):
    try:
        source_elements = browser.find_element(By.CSS_SELECTOR, "input.input-val[data-v-4f2d07f8][type='text'][maxlength='200'][placeholder*='转载视频']")
        source_elements.send_keys('youtube')
        
        time.sleep(10)
    except Exception as e:
        print("An error occurred in bl_add_description:", str(e))

def bl_publish(browser):
    try:
        # Click the publish button
        time.sleep(30)
        submit_button = browser.find_element(By.CSS_SELECTOR, "span.submit-add")
        submit_button.click()
        time.sleep(30)
        print("Clicked the publish button.")
    except Exception as e:
        print("An error occurred in bl_publish:", str(e))

def bl_upload(file_path):
    try:
        browser = bl_browser_initial()
        if browser:
            bl_log(browser)
            browser.get("https://member.bilibili.com/platform/upload/video/frame")
            bl_input_file(browser, file_path)
            bl_add_description(browser,file_path)
            bl_publish(browser)
    except Exception as e:
        print("An error occurred in bl_upload:", str(e))

