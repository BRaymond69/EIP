""" utils.py """
""" Utility functions that can be used by different modules (different ais and/or the dataset/modelisation parts) """


import json
import os

def get_config(path="config.json", module=None):
    with open(path, 'r') as f:
        data = json.load(f)
        if module != None:
            return data[module]
        return data

def fetch_dataset(path, info_path=None):
    """ TODO: Recfactor this if info file is provided in the future """
    categories = os.listdir(path)
    # categories.remove(info_path)
    dataset = {
        c: os.listdir(path + "/" + c) for c in categories
    }
    dataset = {
        c: [(p, list(
                map(int, p.split('_')[-1].split('.')[0].split('x')))
            ) for p in ps if p.split('_')[-1].split('.')[0].count('x') == 2] for c, ps in dataset.items()
    }
    return dataset
