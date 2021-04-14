import requests
from bs4 import BeautifulSoup
import csv

CSV = 'product.csv'
HOST = 'https://zoomagazin.dp.ua/'
URL = 'https://zoomagazin.dp.ua/catalog/sobaki/pitanie-sobak/korma-dlya-sobak/'

HEADERS = {
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-layout')

    products = []

    for item in items:
        products.append(
            {
                'handleId': '',
                'fieldType': 'Product',
                'name': item.find('div', class_='caption').find('a').get_text(strip=True),
                'description': '',
                'img': item.find('div', class_='image').find('a').get('href'),
                'price': item.find('div', class_='kit').find('p').get_text(strip=True)
            }
        )
    return products

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['handleId', 'fieldType', 'name', 'description', 'productImageUrl', 'price'])
        for item in items:
            writer.writerow([item['handleId'], item['fieldType'], item['name'], item['description'], item['img'], item['price']])

def parser():
    PAG = input('How PAGES: ')
    PAG = int(PAG.strip())
    html = get_html(URL)
    if html.status_code == 200:
        products = []
        for page in range(1, PAG):
            print(f'Procesing: {page}')
            html = get_html(URL, params={'page': page})
            products.extend(get_content(html.text))
            save_doc(products, CSV)
        pass
    else:
        print('Err')

parser()

# html = get_html(URL)
# print(get_content(html.text))
