""" utils.py """
""" Utility functions that can be used by different modules (different AIs and/or the dataset/modelisation parts) """

import json
import os
from PIL import Image
import numpy as np

def get_config(path="config.json", module=None):
    with open(path, 'r') as f:
        data = json.load(f)
        if module != None:
            return data[module]
        return data


def fetch_templates(path):
    with open(path, "r") as f:
        refs = json.load(f)
    return refs

def fetch_templates(path=None):
    if path == None:
        path = get_config(module="Modeliser")["Template_refs"]
    with open(path, "r") as f:
        refs = json.load(f)
    return refs

def fetch_dataset(path, info_path=None):
    """ TODO: Recfactor this if info file is provided in the future """
    categories = os.listdir(path)
    refs = fetch_templates()
    # categories.remove(info_path)
    dataset = {
        c: os.listdir(path + "/" + c) for c in categories
    }

    """ Expected format for image files: id_model_WxDxH.jpg """
    """ Output: { "category_path": [("category_path/id_model_WxDxH", model_path, [W, D, H]), ...], ... } """
    def has_correct_format(s):
        if len(s.split('_')) < 2:
            return False
        dims = s.split('_')[-1].split('.')[0]
        model = s.split('_')[-2]
        return dims.count('x') == 2 and model in refs.keys() and model != 'm55'

    def model(s):
        return s.split('_')[-2]

    def dims(s):
        return list(map(int, s.split('_')[-1].split('.')[0].split('x')))

    dataset = {
        c: [(p, model(p), dims(p)) for p in ps if has_correct_format(p)] for c, ps in dataset.items()
    }
    return dataset

def img2pxl(path, dimentions=128, mode="grey", debug=False):
    img = Image.open(path).resize((dimentions, dimentions), Image.ANTIALIAS)
    # for y in arr: sum(map(len, y))
    if debug:
        print("processing %s, mode %s" % (path, img.mode), flush=True)
    process = {
        "grey": {
            "RGB": (lambda im: [[[((int(r) + int(g) + int(b)) / 3) / 0xff] for r, g, b, *_ in list(y)] for y in np.array(im)]),
            "RGBA": (lambda im: [[[((int(r) + int(g) + int(b)) / 3) / 0xff] for r, g, b, *_ in list(y)] for y in np.array(im)]),
            "L": (lambda im: [[[x] for x in y] for y in np.array(im)])
        }
    }
    pixels = process[mode][img.mode](img)
    img.close()

    return pixels
