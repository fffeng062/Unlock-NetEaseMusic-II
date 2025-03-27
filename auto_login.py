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
    browser.add_cookie({"name": "MUSIC_U", "value": "0040597CDC1C94CC59D13B173DACF6181CC0D203AD2475E9E905C0541AC73CE1FB8C7D0E617E82867D15F80C944882C94B62BBA629E587EC10D51D3398FF74F7A717384C4F8A75D9360B53D901CBC0F1E318F1EE88473E3147D4C5F514DC405A3A296BFC918E497BC31D8EE3B6111E2762C10BB8773CC6E7FFAB0EE3E38A1311D754218B41EFB8250404EF9652181F85F131DF31F0B0FDDBB78AF71743EEEFF927A2EC4876E89C0F4EEE12A33DD108455DC412EA1EC73B18512CA7DC94B84B4636954D2489761D567CC9EF55E0F931C3513883CFB2295A6479F0947282797421AC56EFF30DA921EB27AB1385BC1214B1C86A3E6EF02674D16829B17B97CC6F50647E5BB4EBDE226C5B8ED6B86E0F0F6E24EED8B0200AFCF468465C5E9710020E286D042A745622F3AE042ECD7F82017E8AB8B919A68B043CE1EB44E20760179DF7AC75083A631E63483768BAD7FA4A813A6CB3B9DCCEE0ED0ED5CBD9360BA36DD8"})
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
