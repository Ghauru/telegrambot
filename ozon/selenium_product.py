from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from multiprocessing.dummy import Pool
import time
import random
import uuid


class UseSelenium:
    def __init__(self, urls: list, user_id: int):
        self.urls = urls
        self.user_id = user_id

    def save_page(self, url):

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")

        s = Service(executable_path="chromedriver.exe")

        driver = webdriver.Chrome(options=options, service=s)

        try:
            driver.get(url=url)
            time.sleep(5)
            elem = driver.find_element(By.TAG_NAME, "pre").get_attribute('innerHTML')
            time.sleep(random.randrange(3, 10))
            filename = 'product_' + str(uuid.uuid4()) + '.html'
            with open(str(self.user_id) + '/products/' + filename, 'w', encoding='utf-8') as f:
                f.write(elem)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def _save_page_wrapper(self, url):
        return self.save_page(url)

    def multi_save(self):
        p = Pool(processes=10)
        p.map(self._save_page_wrapper, self.urls)
