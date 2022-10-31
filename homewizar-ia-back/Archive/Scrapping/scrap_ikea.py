
import requests
from bs4 import BeautifulSoup
from requests.api import get

root = "https://www.ikea.com/fr/fr/cat/meubles-fu001/"

def get_rq(url, params={}):
    r = requests.get(url, params=params)
    print(r.url)
    encoding = r.encoding if 'charset' in r.headers.get("content-type", "").lower() else None
    return BeautifulSoup(r.content, 'html.parser', from_encoding=encoding)

# s = get_rq(root)
# print(s.prettify().encode('ascii', 'ignore').decode('ascii'))

def parse_link(url):
    if url.split("-")[-1].startswith("fu"):
        s = get_rq(url)
        urls = [a['href'] for a in s.find('div', {'class': 'vn__wrapper'}).find_all('a')]
        for u in urls:
            parse_link(u)
    else:
        print("hi")
        # Will fit all of the furnitures on one page
        # I said will? Oops sorry I meant should >:(
        s = get_rq(url, {'page': '100'})
        print(len(s.prettify()))
        cs = s.find_all('div', {'class': 'plp-product-list__products'})
        print(len(cs))
        cards = cs[1].find_all('div', {'class': 'plp-fragment-wrapper'})
        print(len(cards), len(cs))
        urls = [c.find('a')['href'] for c in cards]
        for u in urls:
            print(u)
        print("done")

parse_link("https://www.ikea.com/fr/fr/cat/meubles-tv-10475/")
