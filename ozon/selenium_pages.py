from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

class UseSelenium:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename

    def save_page(self):

        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")

        s = Service(executable_path="chromedriver.exe")

        driver = webdriver.Chrome(options=options, service=s)

        try:
            driver.get(self.url)
            driver.implicitly_wait(5)
            driver.execute_script("window.scrollTo(5,4000);")
            time.sleep(3)
            html = driver.page_source
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()