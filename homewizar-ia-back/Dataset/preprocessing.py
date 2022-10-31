#!/bin/python3

from sys import argv
from PIL import Image
import numpy as np
import os
import json
from datetime import date
from more_itertools import partition
from pathlib import Path

def usage():
    print("""USAGE
    python preprocessing.py X_X_X/Categorie/

DESCRIPTION
    send as argument the folder of the dataset created to be preprocessed
""")

def get_args():
    if "-h" in argv or len(argv) < 2 or len(argv) >= 3:
        usage()
        exit(0)
    return argv[1:]

def process(image_path, output_path, dimentions=64, visualisation=False):
    img = Image.open(image_path).resize((dimentions, dimentions), Image.ANTIALIAS)
    os.chdir('../../')
    pixels = [[[(int(r) + int(g) + int(b)) / 3] * 3 for r, g, b, *_ in list(y)] for y in np.array(img)]
    out = Image.fromarray(np.array(pixels, dtype=np.uint8))
    out.save(output_path)
    img.close()

    if visualisation:
        out.show()


if __name__ == '__main__':
    root_path, flags = partition(lambda x: x.startswith("-"), get_args())
    root_path = list(root_path)
    flags = list(flags)
    root_path = root_path[0].replace("\\", "")
    root_path = root_path.replace(".", "")

    #### Création du Folder
    processed_path = str(root_path) + "_" + "processed" + "/"
    if not os.path.exists(processed_path):
        os.mkdir(processed_path)
    
    #### Récupération des dossiers
    files = os.listdir(root_path)
    files = list(files)

    #### Ajout du path dans le fichié config.txt
    with open('../config.json', 'r+') as f:
        data = json.load(f)
        data['Dataset']['Save_path'][1] = "Dataset" + '/' + processed_path
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    #### Lancement du Script en boucle dans les fichiers
    for i in files:
        folders = root_path + '/' + i # Path jusqu'au folders
        output_path = processed_path + i # Path des folders de la sortie
        root_pathbis = folders # Path garder en mémoire pour faire les entrée sortie CHDIR
        folders = list(os.listdir(folders))
        nbimages = len(folders)
        dimensions = int(next((x for x in flags if x.startswith("-d=")), "-d=128")[3:])
        print("Generating images with size {}x{}".format(dimensions, dimensions))
        if not os.path.exists(output_path): # Vérification de l'existence des folders d'output
            os.mkdir(output_path)
        for j, img in enumerate(folders):
            os.chdir(root_pathbis)
            output_img_path = output_path + '/' + img
            process(img, output_img_path, dimensions, "-v" in flags)
            print("Progress %i/%i (%.2f%%)" % (j, j, j * 100 / nbimages), end='\r')
            print("Progress %i/%i (%.2f%%)" % (j, nbimages, 100))
        folders = ""
        break
