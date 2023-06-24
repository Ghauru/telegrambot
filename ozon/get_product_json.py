from ozon.selenium_product import UseSelenium


def get_product_links() -> list:
    with open('product_links.txt', 'r', encoding='utf-8') as f:
        return f.readlines()

def data_parsing(products: list, i: int) -> None:
    urls = []
    for i in range(1, i+1):
        filename = 'product_' + str(i) + '.html'
        urls.append('https://www.ozon.ru/api/composer-api.bx/page/json/v2' \
          f'?url={products[i-1]}')
        urls[i-1] = urls[i-1][:-2]
    print(urls)
    UseSelenium(urls, filename).multi_save()

def parse_json():
    products = get_product_links()
    data_parsing(products, len(products))