import os
import json
import time
import emoji
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

print("start to upload to kuaishou")

def ks_browser_initial():
    try:
        browser = webdriver.Chrome()
        browser.get('https://passport.kuaishou.com/pc/account/login/')
        time.sleep(5)
        return browser
    except Exception as e:
        print("Error initializing browser:", str(e))
        return None
 
def ks_log(browser):
    """
    Load cookies from a local file and refresh the page to log in.
    """
    try:
        with open('kuaishou/kuaishou_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        for cookie in listCookies:
            cookie_dict = {
                'domain': '.kuaishou.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            browser.add_cookie(cookie_dict)
        time.sleep(2)
        browser.refresh()
        time.sleep(10)
    except Exception as e:
        print("Error logging in:", str(e))

def remove_special_characters(title):
    try:
        title_without_last_item = title[:title.rfind('[')].strip()
        title_without_emoji = emoji.demojize(title_without_last_item)
        return title_without_emoji
    except Exception as e:
        print("Error removing special characters:", str(e))
        return title

def ks_input_file(browser, file_path):
    try:
        time.sleep(15)
        button = WebDriverWait(browser, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='SOCr7n1uoqI-']")))
        search = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
        search.send_keys(file_path)

        while "上传成功" != browser.find_element(By.CSS_SELECTOR, "span[class='DqNkLCyIyfQ-']").get_attribute("innerHTML"):
            time.sleep(3)
        
        print("Video uploaded successfully.")
    except TimeoutException:
        print("Timeout: Unable to locate the file input element.")
    except Exception as e:
        print("Error uploading video:", str(e))

def ks_add_description(browser,file_path):
    try:
        time.sleep(15)
        file_name = remove_special_characters(os.path.basename(file_path))
        title_input = WebDriverWait(browser, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='clGhv3UpdEo-']"))) 
        title_input.send_keys(file_name)
        time.sleep(10)
        title_input.send_keys("#英语 #英语学习 #tiktok ")
    except Exception as e:
        print("Error adding description:", str(e))

def ks_publish(browser):
    try:
        time.sleep(30)
        WebDriverWait(browser, 150).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='ant-btn ant-btn-primary GncXo-rrppc-']"))).click()
        print("Clicked the publish button.")
        time.sleep(30)
    except Exception as e:
        print("Error clicking publish button:", str(e))

def ks_upload(file_path):
    try:
        browser = ks_browser_initial()
        if browser:
            ks_log(browser)
            browser.get("https://cp.kuaishou.com/article/publish/video")
            ks_input_file(browser, file_path)
            ks_add_description(browser,file_path)
            ks_publish(browser)
    except Exception as e:
        print("Error uploading video:", str(e))

# Example usage:
# ks_upload("path/to/your/video.mp4")
