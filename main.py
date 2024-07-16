import requests
import os
from requests.exceptions import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError('Redirection occurred')
    

def download_book(response, path):
    with open(path, 'wb') as file:
        file.write(response.content)


os.makedirs('books', exist_ok=True)
url = f'https://tululu.org/txt.php'

for book_id in range(1, 11):
    params = {
    'id': book_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        check_for_redirect(response)
    except HTTPError:
        print('Error occured')
        continue

    download_book(response=response,
                  path=f'books/id {book_id}.txt')

    
   