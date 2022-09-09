import random
import time
import os

import requests
from loguru import logger
from utils import stopwatch

is_headless = True
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'


class Requester:
    def __init__(self):
        self.ua = user_agent
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'authorization': 'Bearer',
            'country-id': '12',
            'device': 'pc'
        }
        self.session = requests.Session()
        self.session.headers = self.headers

        logger.debug('Requester session created')

    @stopwatch
    def get(self, url):
        time.sleep(0.5)
        resp = self.session.get(url)
        resp.raise_for_status()

        logger.info(f'Response received, with status code {resp.status_code} - {url}')
        return resp


class Chrome:
    def __init__(self):
        logger.debug('Инициализирую объект Chrome')

        # Selenium
        os.environ['WDM_LOCAL'] = '1'
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--no-sandbox")
        self.option.add_argument("--log-level=3")
        # self.option.add_argument("--start-maximized")
        self.option.add_argument("--window-size=1920,1080")
        self.option.add_argument("--disable-gpu")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.option.add_argument(f"user-data-dir={os.getcwd()}/selenium")
        self.option.add_argument(f'user-agent={user_agent}')
        self.option.headless = is_headless  # True - тихий режим (без интерфейса), False - с интерфейсом браузера
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.option)
        self.driver.set_page_load_timeout = 10

    @stopwatch
    def get_html(self, url):
        try:
            self.driver.get(url)
            source = self.driver.page_source

        except Exception:
            self.driver.quit()
            del self.driver

            self.driver = webdriver.Chrome(options=self.option, executable_path="./chromedriver")
            self.driver.get(url)
            source = self.driver.page_source
        time.sleep(3)
        return source

    def quit(self):
        self.driver.quit()
        return 0
