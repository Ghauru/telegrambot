from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from multiprocessing import Pool


class UseSelenium:
    def __init__(self, urls: list, filename: str):
        self.urls = urls
        self.filename = filename

    def save_page(self):

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument("--headless")

        s = Service(executable_path="chromedriver.exe")

        driver = webdriver.Chrome(options=options, service=s)

        try:
            elem = driver.find_element(By.TAG_NAME, "pre").get_attribute('innerHTML')
            with open('products/' + self.filename, 'w', encoding='utf-8') as f:
                f.write(elem)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def multi_save(self):
        p = Pool(processes=2)
        p.map(UseSelenium.save_page(self), self.urls)
