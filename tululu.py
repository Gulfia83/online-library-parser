import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote
import argparse
from time import sleep



def check_for_redirect(response):
    if response.history:
        raise HTTPError('Redirection occurred')
    

def fetch_book_page(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    page_content = response.text

    return page_content


def parse_book_page(book_url, page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    title_tag = soup.find('h1')
    title, author = title_tag.text.split('::') if title_tag else None
    book_img_src = soup.find(class_='bookimage').find('img')['src']
    img_url = urljoin(book_url, book_img_src) if book_img_src else None

    comments_elements = soup.find_all('div', class_='texts')
    comments = [comment.find('span', class_='black').text for comment in comments_elements]

    genres_elements = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_elements]
    
    book_description = {
        'title': title.strip(),
        'author': author.strip(),
        'comments': [comment for comment in comments],
        'genres': [genre for genre in genres]
    }
    return book_description, img_url


def download_txt(response, title, book_id, folder='books/'):
    sanitized_title = sanitize_filename(title)
    filename = f'{book_id}.{sanitized_title}.txt'
    with open(os.path.join(folder, filename), 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_image(img_url, book_id, folder='images/'):
    response = requests.get(img_url)
    response.raise_for_status()

    split_url = urlsplit(img_url)
    path = unquote(split_url.path)
    extension = path.split('.')[-1] if '.' in path else None
    img_name = f'{book_id}.{extension}' if 'nopic.gif' not in path else 'nopic.gif'
    with open(os.path.join(folder, img_name), 'wb') as file:
        file.write(response.content)


def main():
    parser = argparse.ArgumentParser(
        description='Скачивание книг с сайта tululu.org'
    )
    parser.add_argument('--start_id',
                        type=int,
                        default=1,
                        help='ID книги с которой начать скачивание')
    parser.add_argument('--end_id',
                        type=int,
                        default=10,
                        help='ID книги, которой закончить скачивание')

    args = parser.parse_args()

    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    download_url = 'https://tululu.org/txt.php'

    max_retries = 5

    for book_id in range(args.start_id, args.end_id + 1):
        book_url = f'https://tululu.org/b{book_id}/'
        params = {
            'id': book_id
        }

        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(download_url, params=params)
                response.raise_for_status()
                check_for_redirect(response)

                page_content = fetch_book_page(book_url)
                title, img_url, comments, genres = parse_book_page(book_url, page_content)
                if 'Деловая литература' in genres:
                    download_txt(response,
                            title,
                            book_id)
    
                    download_image(img_url,
                            book_id)
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
        

if __name__ == "__main__":
    main()








