import json
import glob
import re
from ozon.csv_handler import CsvHandler
import sqlite3


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
    return product


def parse_product(id):
    best_choice = {'price': 99999999}
    result_filename = 'ozon_result.csv'
    CsvHandler(result_filename).create_headers_csv_semicolon(['title', 'price', 'photo', 'url'])
    products = get_products()
    for product in products:
        try:
            product_json = get_json(product)
            result = parse_data(product_json)
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(price1, price2, price3, price4, price5) FROM users')
            max_value = cursor.fetchone()[0]
            cursor.execute('''
                SELECT 
                    CASE
                        WHEN MAX(price1, price2, price3, price4, price5) = price1 THEN 'price1'
                        WHEN MAX(price1, price2, price3, price4, price5) = price2 THEN 'price2'
                        WHEN MAX(price1, price2, price3, price4, price5) = price3 THEN 'price3'
                        WHEN MAX(price1, price2, price3, price4, price5) = price4 THEN 'price4'
                        ELSE 'price5'
                    END AS max_column
                FROM users;
            ''')
            max_column_name = cursor.fetchone()[0]
            if result["price"] < max_value:
                if result['price'] < best_choice['price']:
                    best_choice = result
                sql_insert_query = f"UPDATE users SET {max_column_name} = ? WHERE telegram_id = {id}"
                try:
                    cursor.execute(sql_insert_query, (result["price"],))
                    conn.commit()
                except sqlite3.Error as error:
                    print("Ошибка при обновлении данных", error)
                finally:
                    cursor.close()
                    conn.close()
                CsvHandler(result_filename).write_to_csv_semicolon(result)
        except Exception as e:
            print(e)

    return best_choice