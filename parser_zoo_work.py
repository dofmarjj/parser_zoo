import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, "lxml")
    tds = soup.find_all("div", class_="product-layout product-grid col-lg-4 col-md-6 col-sm-6 col-xs-12")
    links = []

    for td in tds[0:5]:
        a = td.find("div", class_="image").find("a").get("href")
        links.append(a)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    try:
        name = soup.find("h1", class_="heading").text.strip()
    except Exception:
        print("Err")

    try:
        price = soup.find("span", class_="autocalc-product-special").text.strip()
    except :
        price = soup.find("span", class_="autocalc-product-price").text.strip()

    data = {'name': name,
            'price': price
            }
    return data

def write_csv(data):
    with open('royal-canin2.csv', 'a') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow((data["name"],
                         data["price"]))
        print(data["name"], "parsed")

def main():
    start = datetime.now()

    url = 'https://zoomagazin.dp.ua/catalog/sobaki/pitanie-sobak/korma-dlya-sobak/royal-canin/?limit=150'
    all_links = get_all_links(get_html(url))

    for url in all_links:
        html = get_html(url)
        data = get_page_data(html)
        write_csv(data)

    end = datetime.now()

    total = end - start
    print(total)

if __name__ == '__main__':
    main()
    
    
    
    ######https://www.youtube.com/watch?v=IGPUs49a1Zo
