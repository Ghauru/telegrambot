from ozon.selenium_pages import UseSelenium
from ozon.link_collector import parse_links
from ozon.get_product_data import parse_product
from ozon.get_product_json import parse_json
import pandas as pd


def parse(url, user_id):
    url = "https://www.ozon.ru/search/?from_global=true&text=" + '+'.join(url.split())

    filename = str(user_id) + '/page.html'
    UseSelenium(url, filename).save_page()
    parse_links(user_id)
    parse_json(user_id)
    parse_product(user_id)
    df = pd.read_csv(str(user_id) +'/ozon_result.csv', sep=',', encoding='utf-8', on_bad_lines='skip')
    sorted_df = df.sort_values(by="price")
    sorted_df.to_csv(str(user_id) + '/ozon_result.csv', index=False)