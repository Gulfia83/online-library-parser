# Parser for the Tululu.org online library
[Russian](RU_README.md)

## Description

Two scripts are presented:

- tululu.py The program allows you to download books from [https://tululu.org/](https://tululu.org/) and save them to your computer. In addition to books (in 'txt' format), the program downloads book covers to the corresponding directories.

- parse_tululu_category.py The program allows you to download books in the "Fiction" category from [https://tululu.org/l55/](https://tululu.org/l55/) and save them to your computer. In addition to books (in 'txt' format), the program downloads book covers. All data on downloaded books, genre and comments are packed into a json file.

## Installation
1. Install Python.
2. Download the code to your computer
3. Install dependencies using `pip` or `pip3`:

```bash
pip install -r requirements.txt
```

## Running the tululu.py script

1. Run the program from the command line.

2. Use the optional arguments --start_id and --end_id to specify a range of book IDs you want to download (the default range is 1 to 10). For example:

```bash
python tululu.py --start_id <start_ID> --end_id <end_ID>
```
Where <start_ID> is the ID of the first book to download, <end_ID> is the ID of the last book.

Example:

```bash
python tulu.py --start_id 20 --end_id 30
```
This will load books with IDs from 20 to 30 inclusive.

After executing the program, the books will be saved in the corresponding directory.

## Running the parse_tululu_category.py script

1. Run the program from the command line.
2. Use optional arguments:
- --start_page Page number to start downloading from
- --end_page Page number to end downloading from
- --skip_imgs Do not download covers
- --skip_txt Do not download books
- --dest_folder path to directory with parsing results: covers, books, JSON

```bash
python tululu.py --start_page <start page> --end_page <end page not inclusive>
```

Example:

```bash
python tulu.py --start_page 700 --end_page 701
```
This will download books from page 700.

After executing the program, the books will be saved in the corresponding directory.

## Project Goals
This code was written to automate the downloading of books for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).