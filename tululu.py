import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote
import argparse



def check_for_redirect(response):
    if response.history:
        raise HTTPError('Redirection occurred')
    

def parse_book_page(url, book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text.split('::')
    title = title_text[0].strip() if title_tag else None

    book_img_src = soup.find(class_='bookimage').find('img')['src']
    img_url = urljoin(url, book_img_src) if book_img_src else None

    comments_elements = soup.find_all('div', class_='texts')
    comments = [comment.find('span', class_='black').text for comment in comments_elements]

    genres_elements = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_elements]

    return title, img_url, comments, genres


def download_txt(response, title, comments, book_id, genres, folder='books/'):
    sanitized_title = sanitize_filename(title)
    filename = f'{book_id}.{sanitized_title}.txt'
    with open(os.path.join(folder, filename), 'w', encoding='utf-8') as file:
        for genre in genres:
            file.write(genre + '\n\n')
        for comment in comments:
            file.write(comment + '\n\n')
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

    download_url = f'https://tululu.org/txt.php'
    url = 'https://tululu.org/'

    for book_id in range(args.start_id, args.end_id + 1):
        book_url = f'https://tululu.org/b{book_id}/'
        params = {
        'id': book_id
        }
        try:
            response = requests.get(download_url, params=params)
            response.raise_for_status()
            check_for_redirect(response)
        except HTTPError:
            continue

        title, img_url, comments, genres = parse_book_page(url, book_url)
        if 'Научная фантастика' in genres:
            download_txt(response,
                    title,
                    comments,
                    book_id,
                    genres)
    
            download_image(img_url,
                    book_id)


if __name__ == "__main__":
    main()








