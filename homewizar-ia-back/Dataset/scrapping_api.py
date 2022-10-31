""" Scrapping using the IKEA api """

import ikea_api
from pwn import wget
import random
import os

constants = ikea_api.Constants(country="fr", language="fr")
categories = [
    "Bibliothèques",
    "Buffet",
    "Bureau",
    "Canapé",
    "Chaise",
    "Commodes",
    "Fauteils",
    "Meubles TV",
    "Tables",
    "Tabouret",
    "Tirroir"
]

def get_funny_name():
    min_len = min(map(len, categories))
    return "".join(random.choice(categories)[i] for i in range(min_len))

def search(search):
    return ikea_api.run(ikea_api.Search(constants).search(search, limit=10000))

def fetch_products():
    samples = []
    folder = get_funny_name()
    os.mkdir(folder)
    print("Output", folder)
    parsed = [] # Avoid duplicats ffs
    for c in categories:
        print(f"Category \"{c}\":", flush=True)
        
        res = search(c)
        products = res['searchResultPage']['products']['main']['items']
        
        hits = len(products) + sum(map(lambda p: p["product"]["gprDescription"]["numberOfVariants"], products))
        print(hits, "hits")
        samples += [hits]

        path = folder + "/" + c
        os.mkdir(path)

        id = 0
        for p in products:
            url = p["product"]["mainImageUrl"]
            if url in parsed:
                print("Skipping")
                continue

            wget(url, path + f"/{id:04}_o_0x0x0.jpg", timeout=120) # We ignore dimentions for now
            id += 1
            parsed += [url]
            for v in p["product"]["gprDescription"]["variants"]:
                url = v["imageUrl"]
                if url in parsed:
                    print("Skipping")
                    continue
                wget(url, path + f"/{id:04}_v_0x0x0.jpg", timeout=120)
                id += 1
                parsed += [url]
            print(f"{id}/{hits}")
        print()

    print(f"Loaded {len(parsed)}/{sum(samples)} samples")

if __name__ == "__main__":
    fetch_products()
