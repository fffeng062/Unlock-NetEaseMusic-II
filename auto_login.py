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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A59C2A4BE03CA78B0C6A40548959E1DD5D68ED36DD25BECD54568372D4E0910D847B6FA292309A245F89C1031112F363F6AEE891B896DF1B60C50E25C18C16311B9E352C17CEA4B0A28D218E48C656BFF3BAC0549F726E6DE0A183CED5F0FCC1709474CBFFBBAD801B999D9A2BD50E39AF7466A0765873589332B7737B4B5CA8DDE48CEC3100F77678D2EC6457B1F28FCFA1104DE4DD2DAC68F0637FFC7C89552D74E52E1D0E14D4607C590A4EE3C257C5DCA8426768DF436EF95023DB0403D6D2F8A4582EB25B5265886AC5A36463F1DEFB173B02B70FB57921A5FC234D5D3B5EFA4A8E48FC8AAA781BF87B79576BC65849575213811DE2DC11AD76D78B28FCA794C80D8A0D2CDD606D8D972FE7F624A670AE314E61993B2EE2F8F30F3600D029DC65B34E45A55FBA2D8C302B39D7A42B169194416EBE27CF0E74AC1407A368202D0BBC12BA546EA35D1B909FCB6C71CFD73FB7FCB6C1B279636EC0408F8293"})
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
