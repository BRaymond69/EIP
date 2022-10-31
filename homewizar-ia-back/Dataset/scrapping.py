from requests_html import HTMLSession
from bs4 import BeautifulSoup
from requests.api import get
import os
import urllib.request
import json
from datetime import date

def get_rq(url, params={}):
    print("Request Start")
    session = HTMLSession()
    r = session.get(url)
    print("Rendering", flush=True)
    r.html.render(sleep=10, timeout=20)
    LinkList = list(filter(lambda v: "/p/" in v, r.html.links))
    print("Request End", flush=True)
    LinkList = list(set(LinkList))
    index = 0
    return (LinkList)

def directory_file(urls):
    dirList = []
    for i in urls:
        i = i.split("/")
        dirList.append(i[6])
    return (dirList)


def isDimensions(dimension):
    if(len(dimension[2].split('x')) == 3):
        return True
    return False

def parse_link(link, dir_list, index):
    request = get(link)
    soup = BeautifulSoup(request.content, "html.parser")

    # Find Dimensions
    all_dims = soup.findAll('div', {"class": "range-revamp-product-dimensions__dimensions-container"})[0].findAll('p', {"class", "range-revamp-product-dimensions__measurement-wrapper"})
    W, H, D = None, None, None
    for dim in all_dims:
        if "Largeur" in str(dim) and W == None:
            W = str(dim).split('<')[-2].split('>')[-1].split(" ")[0]
        if "Hauteur" in str(dim) and H == None:
            H = str(dim).split('<')[-2].split('>')[-1].split(" ")[0]
        if "Profondeur" in str(dim) and D == None:
            D = str(dim).split('<')[-2].split('>')[-1].split(" ")[0]
    if W == None or H == None or D == None:
        return False

    # Find image
    img_url = soup.find('div', {"class": "range-revamp-product__left-top"}).find('img')['src']
    img_url = img_url.split('?')[0]
    print(img_url)
    #print(index, " ", img_url)
    path = dir_list[0] + "/" + str(index) + "_" + W + 'x' + H + 'x' + D + ".jpg"
    urllib.request.urlretrieve(img_url, path)
    return True

def scrap_ikea(url_lists):
    # Date Part
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    dateStr = year + "_" + month + "_" + day
    if not os.path.exists(dateStr):
            os.mkdir(dateStr)
    with open('../config.json', 'r+') as f:
        data = json.load(f)
        data['Dataset']['Save_path'][0] = "Dataset" + '/' + dateStr + '/'
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    # Directory Name + Scrapping Part
    dir_list = directory_file(url_lists)
    index = 0
    for url in url_lists:
        dir_list[0] = dateStr + "/" + dir_list[0]
        print("#############################################")
        print(dir_list[0])
        print("#############################################")
        if not os.path.exists(dir_list[0]):
            os.mkdir(dir_list[0])
        links = get_rq(url)
        for link in links:
            if (parse_link(link, dir_list, index) == True):
                index = index + 1
        dir_list.pop(0)
        index = 0

def get_root_links(root_path):
    path = open(root_path, "r")
    links = path.readlines()
    path.close()
    return links

def main():
    root_links = get_root_links("rootURLs.txt")
    scrap_ikea(root_links)

main()