import json
import glob
import re
from ozon.csv_handler import CsvHandler

def get_products() -> list:
    return glob.glob('products/*.html')

def get_json(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        return json.loads(data)

def parse_data(data: dict) -> dict:
    widgets = data.get('widgetStates')
    for key, value in widgets.items():
        if 'webGallery' in key:
            image_link = json.loads(value).get('coverImage')
        if 'webProductHeading' in key:
            title = json.loads(value).get('title')
        if 'webSale' in key:
            prices = json.loads(value).get('offers')[0]
            if prices.get('price'):
                price = re.search(r'[0-9]+', prices.get('price').replace(u'\u2009', ''))[0]
            else:
                price = 0
    layout = json.loads(data.get('layoutTrackingInfo'))
    url = layout.get('currentPageUrl')
    product = {
        'title': title,
        'price': int(price),
        'photo': image_link,
        'url': url
    }
    print(product)
    return product


def parse_product():
    result_filename = 'ozon_result.csv'
    CsvHandler(result_filename).create_headers_csv_semicolon(['title', 'price', 'photo', 'url'])
    products = get_products()
    for product in products:
        try:
            product_json = get_json(product)
            result = parse_data(product_json)
            CsvHandler(result_filename).write_to_csv_semicolon(result)
        except Exception as e:
            print(e)