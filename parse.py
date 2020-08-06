import os
import requests as req
import csv
from bs4 import BeautifulSoup
from typing import List

# По умолчанию видеокарты
URL = "https://www.regard.ru/catalog/group4000.htm"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
           "accept": "*/*"}
HOST = 'https://www.regard.ru'
FILE = 'information.csv'


# Запрос
def get_html(url, params=None):
    r = req.get(url, headers=HEADERS, params=params)
    return r


# Получение количества страниц товара
def get_page_count(html) -> int:
    soup = BeautifulSoup(html, "html.parser")
    try:
        return int(soup.select('.pagination > a')[-1].text)
    except:
        return 1


# Запись информации в файл
def save_info(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Cсылка', 'Цена в руб.'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])


# Получение названия, ссылки, цены товара
def get_content(html) -> List:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="bcontent")

    objects = []
    i = 0
    for item in items:
        objects.append({
            'title': item.find('a', class_='header').get_text(strip=True),
            'link': HOST + item.find('a', class_='header').get('href'),
            'price': int(item.find_all('span')[3].get_text().replace(' ', ''))
        })
        i += 1
    return objects


# Парсер интернет-магазина regard
def parse():
    try:
        URL: str = input("Введите url: ").strip()
        html = get_html(URL)
    except ValueError:
        URL: str = input("Пожалуйста, введите корректный url: ").strip()
        html = get_html(URL)

    if html:
        items = []
        max_page: int = get_page_count(html.text)
        for page in range(1, max_page + 1):
            print(f"Парсинг страницы {page} из {max_page}...")
            url_page = URL.replace('.htm', f'/page{page}.htm')
            html = get_html(url_page)
            items.extend(get_content(html.text))
        save_info(items, FILE)
        # Запуск файла с информацией о выбранном типе товара
        os.startfile(FILE)
    else:
        print("Error connection!")


parse()
