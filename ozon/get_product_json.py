from ozon.selenium_product import UseSelenium


def get_product_links() -> list:
    with open('product_links.txt', 'r', encoding='utf-8') as f:
        return f.readlines()

def data_parsing(product: str, i: int, filename: str) -> None:
    url = 'https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
          f'?url={product}'

    filename = filename + str(i) + '.html'
    UseSelenium(url, filename).save_page()

def parse_json():
    products = get_product_links()
    i = 1
    for product in products:
        data_parsing(product, i, filename='product_')
        i += 1