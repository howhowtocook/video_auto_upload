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

print("start to upload to douyin")

def dy_browser_initial():
    try:
        browser = webdriver.Chrome()
        browser.get('https://www.douyin.com/user/')
        time.sleep(2) 
        return browser
    except Exception as e:
        print("An error occurred in dy_browser_initial:", str(e))
        return None

def dy_log(browser):
    try:
        with open('douyin/douyin_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        for cookie in listCookies:
            cookie_dict = {
                'domain': '.douyin.com',
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
        time.sleep(3) 
        print("Logged in successfully.")
    except Exception as e:
        print("An error occurred in dy_log:", str(e))

def remove_special_characters(title):
    title_without_last_item = title[:title.rfind('[')].strip()
    title_without_emoji = emoji.demojize(title_without_last_item)
    return title_without_emoji
    
def dy_input_file(browser, file_path):
    try:
        time.sleep(15) 
        input_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        input_element.send_keys(file_path)

        time.sleep(60)
        
        file_name = remove_special_characters(os.path.basename(file_path))
        
        # Find the input element for the title
        title_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.semi-input-default'))
        )
        title_input.send_keys(file_name)
        print("File uploaded successfully.")
    except Exception as e:
        print("An error occurred in dy_input_file:", str(e))

def dy_add_tags(browser, times):
    try:
        time.sleep(20)
        for _ in range(times):
            time.sleep(2)  # Wait for 1 second
            # Find the list container element
            list_container = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list--AaGTY'))
        )
        
            # Find the first element in the list
            first_element = list_container.find_element(By.XPATH, './div[1]')

            # Click the first element
            first_element.click()
            
        
        print("Tags added successfully.")
    except Exception as e:
        print("An error occurred in dy_add_tags:", str(e))

def dy_publish(browser):
    try:
        time.sleep(10)
        publish_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button--1SZwR.primary--1AMXd.fixed--3rEwh'))
        )
        publish_button.click()
        time.sleep(30)
        
        print("Video published successfully.")
    except Exception as e:
        print("An error occurred in dy_publish:", str(e))


def dy_upload(file_path):
    try:
        browser = dy_browser_initial()
        if browser:
            dy_log(browser)
            browser.get("https://creator.douyin.com/creator-micro/content/upload")
            dy_input_file(browser, file_path)
            dy_add_tags(browser, 5)
            dy_publish(browser)
    except Exception as e:
        print("An error occurred in dy_upload:", str(e))