
import json
from PIL import Image
import numpy as np

class ParseDatahubDataset:

    def __init__(self, path="datasets/target-furniture-2/Target_Furniture_Collections_Dataset/", test=False):
        self.path = path
        self.datapath = "furniture_collection_images/"
        self.categories = set()
        self.ref = {}

        if test:
            return

        with open(self.path + "category_ID_mapping.json", "rb") as f:
            for k, v in json.loads(f.read()).items():
                self.ref[k] = v.split(" | ")
                for c in v.split(" | "):
                    self.categories.add(c)
        print(len(self.categories), len(self.ref))
        print(self.categories)

    def parseFile(file, w, h):
        with Image.open(file).resize((w, h), Image.ANTIALIAS) as img:
            pixels = [[[(int(r) + int(g) + int(b)) / 3] for r, g, b, *_ in list(y)] for y in np.array(img)]
        return pixels

    def getNext(self, width=400, height=400):
        prefix = self.path + self.datapath
        for img in self.ref.keys():
            yield ParseDatahubDataset.parse_file(prefix + img, width, height)

if __name__ == '__main__':
    dt = ParseDatahubDataset()
