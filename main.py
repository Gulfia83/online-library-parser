import requests
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote



def check_for_redirect(response):
    if response.history:
        raise HTTPError('Redirection occurred')
    

def get_book_title(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    if title_tag:
        title_text = title_tag.text.split('::')
        title = title_text[0].strip()
    else:
        print("Не удалось найти заголовок.")

    return title


def get_image_url(book_url):
    base_url = 'https://tululu.org'
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_image_src = soup.find(class_='bookimage').find('img')['src']
    if book_image_src:
        image_url = urljoin(base_url, book_image_src)
    else:
        print("Не удалось найти ссылку на картинку")

    return image_url


def download_txt(response, title,book_id, folder='books/'):
    sanitized_title = sanitize_filename(title)
    filename = f'{book_id}.{sanitized_title}.txt'
    with open(os.path.join(folder, filename), 'wb') as file:
        file.write(response.content)


def download_image(image_url, book_id, folder='images/'):
    response = requests.get(image_url)
    response.raise_for_status()

    split_url = urlsplit(image_url)
    path = unquote(split_url.path)
    extension = path.split('.')[-1] if '.' in path else None
    image_name = f'{book_id}.{extension}' if 'nopic.gif' not in path else 'nopic.gif'
    with open(os.path.join(folder, image_name), 'wb') as file:
        file.write(response.content)

os.makedirs('books', exist_ok=True)
os.makedirs('images', exist_ok=True)

download_url = f'https://tululu.org/txt.php'

for book_id in range(1, 11):
    book_url = f'https://tululu.org/b{book_id}/'
    params = {
    'id': book_id
    }
    try:
        response = requests.get(download_url, params=params)
        response.raise_for_status()
        check_for_redirect(response)
    except HTTPError:
        print('Error occured')
        continue

    title = get_book_title(book_url)
    download_txt(response,
                  title,
                  book_id)
    image_url = get_image_url(book_url)
    download_image(image_url,
                   book_id)