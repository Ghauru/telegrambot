from ozon.selenium_product import UseSelenium


def get_product_links(user_id) -> list:
    with open(str(user_id) + '/product_links.txt', 'r', encoding='utf-8') as f:
        return f.readlines()


def data_parsing(products: list, i: int, user_id: int) -> None:
    urls = []
    for j in range(1, i+1):
        urls.append('https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
          f'?url={products[j-1]}')
        urls[j-1] = urls[j-1][:-2]
    UseSelenium(urls, user_id).multi_save()


def parse_json(user_id):
    products = get_product_links(user_id)
    data_parsing(products, len(products), user_id)
