import os
import json
import time
import emoji
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

print("start to upload to xiaohongshu")

def xhs_browser_initial():
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.xiaohongshu.com/explore')
        time.sleep(2)
        return browser
    except Exception as e:
        print("Error initializing browser:", str(e))
        return None
 
def xhs_log(browser):
    try:
        with open('xiaohongshu/xiaohongshu_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        for cookie in listCookies:
            cookie_dict = {
                'domain': '.xiaohongshu.com',
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
        browser.refresh()
        time.sleep(10)
    except Exception as e:
        print("Error logging in:", str(e))

def remove_special_characters(title):
    try:
        if '[' in title:
            title_without_last_item = title[:title.rfind('[')].strip()
        else:
            title_without_last_item = title
        title_without_emoji = emoji.demojize(title_without_last_item)
        # Ensure the length of the title does not exceed 20 characters
        if len(title_without_emoji) > 20:
            title_without_emoji = title_without_emoji[:18]
        return title_without_emoji
    except Exception as e:
        print("Error removing special characters:", str(e))
        return title

def xhs_input_file(browser, file_path):
    try:
        time.sleep(30)
        search = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
        search.send_keys(file_path)
        time.sleep(60)
        print("Video added successfully.")
    except TimeoutException:
        print("Timeout: Unable to locate the file input element.")
    except Exception as e:
        print("Error uploading video:", str(e))

def xhs_add_description(browser,file_path):
    try:
        file_name = remove_special_characters(os.path.basename(file_path))
        title_input = browser.find_element(By.CSS_SELECTOR, "input[class='c-input_inner']")
        title_input.send_keys(file_name)
        time.sleep(10)
        tag_input = browser.find_element(By.CSS_SELECTOR, "p[id='post-textarea']")
        tag_input.send_keys("#英语 #英语学习 #tiktok #学习英语 #英语轻松学")
        print('description added successfully')
    except Exception as e:
        print("Error adding description:", str(e))

def xhs_publish(browser):
    try:
        time.sleep(30)
        submit = browser.find_element(By.CSS_SELECTOR, "button.css-k3hpu2.css-osq2ks.dyn.publishBtn.red")
        submit.click()
        time.sleep(40)
        print("Clicked the publish button.")
    except Exception as e:
        print("Error clicking publish button:", str(e))

def xhs_upload(file_path):
    try:
        browser = xhs_browser_initial()
        if browser:
            xhs_log(browser)
            browser.get("https://creator.xiaohongshu.com/publish/publish")
            xhs_input_file(browser, file_path)
            xhs_add_description(browser,file_path)
            xhs_publish(browser)
            time.sleep(10)
    except Exception as e:
        print("Error uploading video:", str(e))

# Example usage:
# xhs_upload("path/to/your/video.mp4")
