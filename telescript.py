import requests
import os

image_file = 'RN.png'

upload_url = 'https://api.ozon.ru/composer-api.bx/upload-file'
fileobj = open(image_file, 'rb')
files = {'file': (os.path.basename(image_file), fileobj)}

response = requests.post(upload_url, files=files)
file_id = response.json()['result']['id']
fileobj.close()

search_url = 'https://api.ozon.ru/composer-api.bx/page/json/v2'
headers = {'User-Agent': 'Mozilla/5.0'}
params = {'url': f'/category/search?from=suggest&imageUrl={file_id}&noSerp=true'}

response = requests.get(search_url, headers=headers, params=params)
results = response.json()

for item in results['data']['content']['items']:
    print('Название:', item['title'])
    print('Цена:', item['price']['value'])
    print('Рейтинг:', item['rating'])
    print('Ссылка на страницу товара:', item['href'])