#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import sys
import time
import os

def scraping(url):
    url_split = url.split('/')[6].replace('-', '_') + '_'
    print(url_split)
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.findAll('div',{'class': 'range-revamp-product-dimensions__list-container'})
        size = []
        for i in div:
            for word in i:
                spliter = str(word).split('>')[1].split(' ')[0]
                if spliter.isdigit():
                    size.append(spliter)
        size = size[:3]
        source = []
        x = 0
        good = False
        string = 'https://www.ikea.com/fr/fr/images/products'
        download_link = ""
        for raw_img in soup.find_all('img'):
            link = raw_img.get('src')
            source.append(link)
            source = list(filter(None, source))
            while x != len(source):
                if good != True:
                    good = source[x].startswith(string)
                    download_link = source[x]
                x+=1
        img_data = requests.get(download_link).content
        width = size[0]
        depth = size[1]
        height = size[2]
        image = url_split + '_' + str(width) + '-' + str(height) + '-' + str(depth) + '.jpg'
        print(image)
        with open(image, 'wb') as handler:
            handler.write(img_data)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ./scrapping.py")
    with open(sys.argv[1], 'r') as fd:
        buff = fd.read().rstrip().split('\n')
        for i in buff:
            scraping(i)
