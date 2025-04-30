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
    browser.add_cookie({"name": "MUSIC_U", "value": "00811EB7535C30DAFE70590D80DD0149512AD4DB5D52894A2F0E5D20FDEF7EBA0FFA8C8412A507914DD515A7D8B8DA4CB4605E6925C3EA66E42AA51D754136B46834775240F55A64D5322BA9DA202E2F0B699BDAE7CF090CCEED9A0F27183B05FDDEC1DCAA0798716201F5A69FB27508861391C7B2EE40D31505A42B1500C2605709ED9DC2266AEC79003822D9CDE7D9CA5EC6B349A4F2F958040D5DD2699EE40F8C93063EEF409CF03779D99550DFC34E58021B530020CDCE6512A3206EB4B8075D0DB58BEA007EEC19F5E14F4A7F5F0BFF2F7F5992C0F3B6C8C0DC2BECA2944CFAE3CF8359305E31693F25142523C3BDF9084D0E550DA9ED26D53FD64F3DBF37C0B6191A02B01E8BCE27D524E01CC100B0E268CF51E1B88AE65A967839CF61EC60B6986B131CDE81B2A6A46099443814D3786C13A5E59EB4F6FBE117994057C31BDBE719DB0829C6AD20C81588C719A6142BA21D4E27C984F57A0A79C8E20582"})
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
