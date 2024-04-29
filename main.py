import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com'

def get_quotes():
    all_quotes = []
    page = 1
    while True:
        response = requests.get(f'{BASE_URL}/page/{page}')
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        if not quotes:
            break
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            author_link = quote.find('small', class_='author').find_next('a')['href']
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            all_quotes.append({'quote': text, 'author': author, 'author_link': author_link, 'tags': tags})
        page += 1
    return all_quotes

def get_authors():
    quotes = get_quotes()
    authors = []
    for quote in quotes:
        author_info = requests.get(BASE_URL + quote['author_link'])
        author_soup = BeautifulSoup(author_info.content, 'html.parser')
        born_date = author_soup.find('span', class_='author-born-date').text.strip()
        born_location = author_soup.find('span', class_='author-born-location').text.strip()
        description = author_soup.find('div', class_='author-description').text.strip()
        author_data = {
            'fullname': quote['author'],
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }
        authors.append(author_data)
    return authors

# Отримуємо цитати
quotes = get_quotes()

# Записуємо цитати у файл quotes.json
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=4)

# Отримуємо дані про авторів
authors = get_authors()

# Записуємо дані про авторів у файл authors.json
with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors, f, ensure_ascii=False, indent=4)



