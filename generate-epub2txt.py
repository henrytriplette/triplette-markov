#!/usr/bin/env python
# Main script for converting *.epub into *.txt for processing
import argparse
import os
import random
import time
import ebooklib

from datetime import datetime
from ebooklib import epub
from bs4 import BeautifulSoup

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head',
	'input',
	'script',
	# there may be more elements you don't want, such as "style", etc.
]

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    output = []
    for html in thtml:
        text =  chap2text(html)
        output.append(text)
    return output

def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

def content2txt(content, file):
    filepath = file + ".txt"
    f = open( filepath, 'a')
    f.truncate()
    # Compact content
    f.write(','.join(content))
    f.close()

    return filepath

def main(file_list):

    # Process files
    for file in file_list:
        # Read
        content = epub2text(file)
        # Write
        converted_file_path = content2txt(content, file)
        # Log
        print(converted_file_path)

if __name__ == '__main__':

    # Initialize
    parser = argparse.ArgumentParser(description='Convert epub to txt.')
    parser.add_argument('-f', '--folder', help='Source images folder', required=True)

    args = parser.parse_args()

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(args.folder):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    listOfBooks = list()
    for elem in listOfFiles:
        if elem.lower().endswith(('.epub')):
            listOfBooks.append(elem)

    try:
        main(listOfBooks)
    except KeyboardInterrupt:
        print('Ended!')
