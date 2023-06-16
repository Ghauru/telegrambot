from bs4 import BeautifulSoup
import glob

def get_pages() -> list:
    return glob.glob('page.html')

def get_html(page: str):
    with open(page, 'r', encoding='utf-8') as f:
        return f.read()

def parse_data(html: str) -> str:
    links = []
    with open("page.html", encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        div1 = soup.select("div.widget-search-result-container > div > div")
        div1 = str(div1)
        div1 = div1[div1.find("\""):div1.find(">")]
        div1 = div1.split()[0][1:]

        products = soup.find("div", attrs={"class", "widget-search-result-container"}).find_all("a")
        print(products)
        for product in products:
            links.append(product.get('href').split('?')[0])
    print(links)
    return set(links)

def parse_links():
    pages = get_pages()

    all_links = []

    for page in pages:
        html = get_html(page)
        links = parse_data(html)
        all_links = all_links + list(links)

    with open('product_links.txt', 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(str(link) + '\n')