from ozon.selenium_product import UseSelenium


def get_product_links(user_id) -> list:
    with open(str(user_id) + '/product_links.txt', 'r', encoding='utf-8') as f:
        return f.readlines()


def data_parsing(products: list, i: int, user_id: int) -> None:
    urls = []
    for i in range(1, i+1):
        urls.append('https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
          f'?url={products[i-1]}')
        urls[i-1] = urls[i-1][:-2]
    for i in range(1, i+1):
        filename = 'product_' + str(i) + '.html'
        use_selenium = UseSelenium(urls, filename, user_id)
        use_selenium.multi_save()


def parse_json(user_id):
    products = get_product_links(user_id)
    data_parsing(products, len(products), user_id)
