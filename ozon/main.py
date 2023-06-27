from ozon.selenium_pages import UseSelenium
from ozon.link_collector import parse_links
from ozon.get_product_data import parse_product
from ozon.get_product_json import parse_json
import pandas as pd


def parse(url, user_id):
    url = "https://www.ozon.ru/search/?from_global=true&text=" + '+'.join(url.split())

    MAX_PAGE = 10
    i = 1
    while i <= MAX_PAGE:
        filename = str(user_id) + f'/pages/page_' + str(i) + '.html'
        if i == 1:
            UseSelenium(url, filename).save_page()
        else:
            url_param = url + '?page=' + str(i)
            UseSelenium(url_param, filename).save_page()
        i += 1
    filename = str(user_id) + '/page.html'
    UseSelenium(url, filename).save_page()
    parse_links(user_id)
    parse_json(user_id)
    parse_product(user_id)
    df = pd.read_csv(str(user_id) +'/ozon_result.csv', sep=',', encoding='utf-8', on_bad_lines='skip')
    sorted_df = df.sort_values(by="price")
    sorted_df.to_csv(str(user_id) + '/ozon_result.csv', index=False)
    df = pd.read_csv(str(user_id) +'/ozon_result.csv', sep=',', encoding='utf-8', on_bad_lines='skip')
    df.drop_duplicates(inplace=True)
    df.to_csv(str(user_id) + '/ozon_result.csv', index=False)

