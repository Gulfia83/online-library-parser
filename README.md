# Parser for the Tululu.org online library
[Russian](RU_README.md)

## Description
This program is designed to download science fiction books from the site tululu.org. You can select a range of book IDs to download and the program will download them for you.

## Installation
1. Install Python.
2. Download the code to your computer
3. Install dependencies using `pip` or `pip3`:

```bash
pip install -r requirements.txt
```

## Usage
1. Run the program from the command line.
2. Use the optional arguments --start_id and --end_id to specify the range of book IDs you want to download (default range is 1 to 10). For example:

```bash
python tululu.py --start_id <start_ID> --end_id <end_ID>
```
Where <start_ID> is the identifier of the first book to download, <end_ID> is the identifier of the last book.

Example:

```bash
python tulu.py --start_id 20 --end_id 30
```
This will load books with IDs from 20 to 30 inclusive, if the book genre is Science Fiction.

After executing the program, books will be saved in the books/ directory, and covers - in the images/ directory.

## Overview of program capabilities
### Function ``check_for_redirect(response)``
This function checks whether a redirect occurred when attempting to download a book. If a redirection occurs, the function raises an error.

### Function ``parse_book_page(url, book_url)``
This function parses the book page on tululu.org and extracts the following information:

- Book title
- Link to book cover
- Comments about the book
- Genres of the book

### Function ``download_txt(response, title, comments, book_id, genres, folder='books/')``
This function downloads the text of a book and saves it to a file with a name based on the book's ID and title. Also, the genre of the book and comments about the book are added to the beginning of the file.

### Function ``download_image(img_url, book_id, folder='images/')``
This function downloads the book cover and saves it to a specified directory with a file name based on the book ID.

## Project goals
This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).