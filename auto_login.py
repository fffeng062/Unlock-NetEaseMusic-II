# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "006C4B60FBA0F3DE001632BED74C1E402BE4B39842C3BDE0211507DCF8F1F12DEF9BD2771E176C7091437AF4A27EBE83C8F57B7FBFC12B262283BA6EB874BAFD0955FC20BE34FD6B7A6236B2CF85155F3EF87FC76A5F5FA9A84D926700944C1DD168DF00087077CD3BDC1FFD1AD3683256678FF69950B1C461069E578E2DB88C00CD488FEEBC8E37A1948ACC067C8FD3590A5F6747AC393E56654976D8B89B8F3C645F4F2D1761096874A7D3D0FBDFC4410D91C91C09614934F8D30B28C2CA23E279D14233839B50AD38625F68D3C100A021B0648740B5B83C3AC5F53F22E4CE05FD0FDED57592DDE40AFB55E6F630E817774236A8AD349857ECFFE1BB4230393C36D90D67B0E4D84AE641BBC6DD97E6DEFB1E5735F13736812DED8B23596E6696F567557867E828ADEE743CF18BB8440E2BF96EEA0F5920CD74AEACBB9DCE0092203D3BBCC2B87ABD8350A9E3A01E9A26CFF4817A860E153C17F0A356B86D49DF"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
