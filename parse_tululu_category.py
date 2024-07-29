import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, unquote
from tululu import check_for_redirect, download_image, download_txt, parse_book_page
import json
from time import sleep


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    return response.text


def fetch_books_urls(url, page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    book_elements = soup.select('.d_book .bookimage a')
    book_urls_src = [book_element['href'] for book_element in book_elements]
    books_urls_per_page = []
    for book_url_src in book_urls_src:
        book_url = urljoin(url, book_url_src)
        books_urls_per_page.append(book_url)

    return books_urls_per_page


os.makedirs('books', exist_ok=True)
os.makedirs('images', exist_ok=True)

download_url = 'https://tululu.org/txt.php'

books_urls = []
books_descriptions = []
for page in range(1, 2):
    page_url = f'https://tululu.org/l55/{page}'
    page_content = fetch_page(page_url)
    books_urls.extend(fetch_books_urls(page_url, page_content))

max_retries = 5

for book_url in books_urls:
    split_book_url = urlsplit(book_url)
    path = unquote(split_book_url.path)
    book_id = path[2:-1]
    params = {
        'id': book_id
    }
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(download_url, params=params)
            response.raise_for_status()
            check_for_redirect(response)
            book_page_content = fetch_page(book_url)
            book_description, img_url = parse_book_page(book_url, book_page_content)
            title = book_description['title']
            book_description['book_path'] = download_txt(response,
                                                         title,
                                                         book_id)
            book_description['img_src'] = download_image(img_url,
                                                         book_id)
            books_descriptions.append(book_description)
            break
             
        except HTTPError:
            print(f'Redirection occured from {book_url} to {response.url}')
            break

        except requests.ConnectionError:
            retries += 1
            print(f'Connection error for book {book_id}')
            sleep(5)

    else:
        continue
  
    with open('books_descriptions.json', 'w', encoding='utf8') as json_file:
        json.dump(books_descriptions, json_file, indent=4, ensure_ascii=False)
