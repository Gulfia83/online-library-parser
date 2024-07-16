import requests
import os


def download_book(url, path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


os.makedirs('books', exist_ok=True)
url = f'https://tululu.org/txt.php'


for book_id in range(1, 11):
    params = {
    'id': book_id
    }
    download_book(url=url,
                  path=f'books/id {book_id}.txt',
                  params=params)
