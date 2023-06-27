from bs4 import BeautifulSoup
import glob


def get_pages(user_id) -> list:
    return glob.glob(str(user_id) + '/pages/*.html')


def get_html(page: str):
    with open(page, 'r', encoding='utf-8') as f:
        return f.read()


def parse_data(html: str) -> str:
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find("div", attrs={"class", "widget-search-result-container"}).find_all("a")
    for product in products:
        links.append(product.get('href').split('?')[0])
    return set(links)


def parse_links(user_id):
    pages = get_pages(user_id)

    all_links = []

    for page in pages:
        html = get_html(page)
        links = parse_data(html)
        all_links = all_links + list(links)

    with open(str(user_id) + '/product_links.txt', 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(str(link) + '\n')
