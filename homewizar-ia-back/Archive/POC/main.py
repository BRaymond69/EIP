#!/usr/bin/python3


import sys, os, math
# import tensorflow as tf
import pandas as pd
import numpy as np 


coordinates = {}
def get_cood(args):
    img = []
    for i in args:
        # print(i)
        img.append(i)
        first_split = i.split('-')
        element_split = first_split[1]
        element = element_split.split('_')
        x = element[0]
        y = element[1]
        z = element[2][:2]
        coordinates[first_split[0]] = {"Coordinate x": int(x), "Coordinate y": int(y), "Coordinate z": int(z)}

def main(args):
    coordinates = get_cood(args)
    # print(coordinates)

if __name__ == "__main__":
    main(sys.argv[1:])
    pass