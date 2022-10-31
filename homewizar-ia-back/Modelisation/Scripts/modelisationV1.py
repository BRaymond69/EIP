import json
import os
import random
from unicodedata import name

def isCategory(category):
    return os.path.exists("modelization/Modelisation/Templates/"+category)

def createGlbPathList(category):
    glb_list = []
    for file in os.listdir("modelization/Modelisation/Templates/"+category):
        if ".glb" in file:
            glb_list.append(file)
    return (glb_list)

def getGlbId(loaded_json, glb):
    for glb_name in loaded_json:
        if (glb_name.get("name") == glb):
            return (glb_name.get("id"))
    return (-1)
        

def chooseRandomGlb(glb_list, config):
    json_file = open(config)
    id_product = json.load(json_file)
    random_glb = random.choice(glb_list)
    chosen_glb = getGlbId(id_product, random_glb)

    json_file.close()
    return (chosen_glb)

def modelisation(category, config):
    if (isCategory(category) == False):
        print("This category", category, "doesn't exist!")
        return(-1)
    return (chooseRandomGlb(createGlbPathList(category), config))
