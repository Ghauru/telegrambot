from ozon.selenium_pages import UseSelenium
from ozon.link_collector import parse_links
from ozon.get_product_data import parse_product
from ozon.get_product_json import parse_json

def parse(url):
    url = "https://www.ozon.ru/search/?from_global=true&text=" + '+'.join(url.split())

    filename = 'page.html'
    UseSelenium(url, filename).save_page()
    parse_links()
    parse_json()
    parse_product()
