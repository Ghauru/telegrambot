import asyncio
import json
import glob
import re
from ozon.csv_handler import CsvHandler
import sqlite3


def get_products(user_id) -> list:
    return glob.glob(str(user_id) + '/products/*.html')


def get_json(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        return json.loads(data)


def parse_data(data: dict) -> dict:
    widgets = data.get('widgetStates')
    image_link = None
    title = None
    price = None
    for key, value in widgets.items():
        if value is not None:
            if 'webGallery' in key:
                image_link = json.loads(value).get('coverImage')
            if 'webProductHeading' in key:
                title = json.loads(value).get('title')
            if'webPrice' in key:
                if 'price' in json.loads(value):
                    price = re.search(r'[0-9]+', json.loads(value)['price'].replace(u' ', '')).group()
                else:
                    price = 999999999
    layout = json.loads(data.get('layoutTrackingInfo'))
    url = layout.get('currentPageUrl')
    product = {
        'title': title,
        'price': int(price) if price is not None else 999999999,
        'photo': image_link,
        'url': url
    }
    return product


async def parse_product(user_id):
    await asyncio.sleep(0.1)

    result_filename = str(user_id) + '/ozon_result.csv'
    CsvHandler(result_filename).create_headers_csv_semicolon(['title', 'price', 'photo', 'url'])
    products = get_products(user_id)

    for product in products:
        try:
            product_json = get_json(product)
            result = parse_data(product_json)
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT price FROM users WHERE telegram_id = "{user_id}"')
            price = cursor.fetchone()[0]
            cursor.execute(
                f'SELECT MAX(price1, price2, price3, price4, price5) FROM users WHERE telegram_id = "{user_id}"')
            max_value = cursor.fetchone()[0]
            cursor.execute(f'''
                   SELECT 
                       CASE
                           WHEN MAX(price1, price2, price3, price4, price5) = price1 THEN 'price1'
                           WHEN MAX(price1, price2, price3, price4, price5) = price2 THEN 'price2'
                           WHEN MAX(price1, price2, price3, price4, price5) = price3 THEN 'price3'
                           WHEN MAX(price1, price2, price3, price4, price5) = price4 THEN 'price4'
                           ELSE 'price5'
                       END AS max_column
                   FROM users WHERE telegram_id = "{user_id}";
               ''')
            max_column_name = cursor.fetchone()[0]
            if result['price'] > price:
                if result['price'] < max_value:
                    photo_url = 'photo_url' + max_column_name[-1]
                    photo = result['photo']
                    sql_insert_query = f'UPDATE users SET "{photo_url}" = "{photo}" WHERE telegram_id = "{user_id}"'
                    try:
                        cursor.execute(sql_insert_query)
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при обновлении данных1", error)
                    name = 'name' + max_column_name[-1]
                    title = result['title']
                    name = name.replace('\'', '').replace('"', '')
                    sql_insert_query = f'UPDATE users SET "{name}" = "{title}" WHERE telegram_id = "{user_id}"'
                    try:
                        cursor.execute(sql_insert_query)
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при обновлении данных2", error)
                    link = 'link' + max_column_name[-1]
                    url = result['url']
                    sql_insert_query = f'UPDATE users SET "{link}" = "{url}" WHERE telegram_id = "{user_id}"'
                    try:
                        cursor.execute(sql_insert_query)
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при обновлении данных3", error)
                    sql_insert_query = f"UPDATE users SET {max_column_name} = ? WHERE telegram_id = {user_id}"
                    try:
                        cursor.execute(sql_insert_query, (result["price"],))
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Ошибка при обновлении данных4", error)
                    finally:
                        cursor.close()
                        conn.close()
            CsvHandler(result_filename).write_to_csv_semicolon(result)
        except Exception as e:
            print(e)
    await asyncio.sleep(0.1)
