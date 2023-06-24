from ozon.selenium_pages import UseSelenium
from ozon.link_collector import parse_links
from ozon.get_product_data import parse_product
from ozon.get_product_json import parse_json
import pandas as pd

def parse(url, id):
    url = "https://www.ozon.ru/search/?from_global=true&text=" + '+'.join(url.split())

    filename = 'page.html'
    UseSelenium(url, filename).save_page()
    parse_links()
    parse_json()
    best_choice = parse_product(id)
    df = pd.read_csv('ozon_result.csv', sep=',', encoding='utf-8', on_bad_lines='skip')
    sorted_df = df.sort_values(by="price")
    sorted_df.to_csv('ozon_result.csv', index=False)
    df.drop(df.head(len(df) - 5).index, inplace=True)
    df.to_csv('ozon-result.csv', index=False)
    return best_choice