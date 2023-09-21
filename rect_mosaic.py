import pathlib
import json
import os
import math
import random
import sys

import numpy as np
import cv2

def get_average_color(img):
    average_color = np.average(np.average(img, axis=0), axis=0)
    average_color = np.around(average_color, decimals=-1)
    average_color = tuple(int(i) for i in average_color)
    return average_color

def get_closest_color(color, colors):
    cr, cg, cb = color

    min_difference = float("inf")
    closest_color = None
    for c in colors:
        r, g, b = eval(c)
        difference = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        if difference < min_difference:
            min_difference = difference
            closest_color = eval(c)

    return closest_color

if "tmp/cache.json" not in os.listdir():
    imgs_dir = pathlib.Path("dataset")
    images = list(imgs_dir.glob("*//*.jpg"))

    data = {}
    for img_path in images:
        img = cv2.imread(str(img_path))
        average_color = get_average_color(img)
        if str(tuple(average_color)) in data:
            data[str(tuple(average_color))].append(str(img_path))
        else:
            data[str(tuple(average_color))] = [str(img_path)]
    with open("tmp/cache.json", "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
    print("Caching done")

with open("tmp/cache.json", "r") as file:
    data = json.load(file)

tile_width = int(input("Width for tiles: (10 is default) "))
tile_height = int(input("Height for tiles: (10 is default) "))


# Change the input image directory here
img = cv2.imread("img.jpg")
img_height, img_width, _ = img.shape
num_tiles_h, num_tiles_w = img_height // tile_height, img_width // tile_width
img = img[:tile_height * num_tiles_h, :tile_width * num_tiles_w]

tiles = []
for y in range(0, img_height, tile_height):
    for x in range(0, img_width, tile_width):
        tiles.append((y, y + tile_height, x, x + tile_width))

for tile in tiles:
    y0, y1, x0, x1 = tile
    try:
        average_color = get_average_color(img[y0:y1, x0:x1])
    except Exception:
        continue
    closest_color = get_closest_color(average_color, data.keys())

    i_path = random.choice(data[str(closest_color)])
    i = cv2.imread(i_path)
    i = cv2.resize(i, (tile_width, tile_height))
    img[y0:y1, x0:x1] = i

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.imwrite("outputs/rectangle/rect_output.jpg", img)