import pathlib
import json
import os
import math
import random
import sys
from PIL import Image, ImageDraw

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

def mask(x,y,r,size):
    '''This function generate a mask image.
    x,y indicate the center of the circle, r= diameter (correction)
    size = size of the image which will be cropped'''
    x1=x-r/2
    y1=y-r/2
    x2=x+r/2
    y2=y+r/2
    image = Image.new('L', size, color="black")
    draw = ImageDraw.Draw(image)
    #draw ellipse actually draw a rectangular region here x1,y1,x2,y2
    #define region of a circle.
    draw.ellipse((x1,y1, x2, y2), fill = 'white', outline ='white')
    return image

def saveCropped(image_pix, mask_img, image, img_height, img_width):
    mask_pix = mask_img.load()
    W,H = mask_img.size

    for y in range(H):
        for x in range(W):
            value=mask_pix[x,y]
            if value==0:
                image_pix[x,y]=(0,0,0,0) #set transparent value
    y=img_width/2 - (img_height if img_width > img_height else img_width) / 2
    x=0
    h=img_height
    w=img_height

    box = (y, x, y+h, x+w)
    img2 = image.crop(box)
    img2.save("tmp/temp_croped_image.png")
    return img2

def reshapeImage (i_path):
    # print("Reshaping start")

    image=Image.open(i_path).convert("RGBA") #open the image
    image_pix=image.load()

    img = cv2.imread(str(i_path))
    img_height, img_width, _ = img.shape

    mask_img=mask(img_width/2, img_height/2, img_height if img_height < img_width else img_width, image.size) 
        #input your mouse position instead of 500,400
        #here 100 is radius of the circle you can modify it

    return saveCropped(image_pix, mask_img, image, img_height, img_width)
    
def score(image, img, y0, y1, x0, x1):

    height, width, _ = image.shape
    for i in range(height):
        for j in range(width):
            if all(image[i, j] == [0,0,0]):
                image[i, j] = img[y0 + i, x0 + j]

# if "crops/croped_image0/png" not in os.listdir():
#     reshapeImage()

if "tmp/cache.json" not in os.listdir():
    imgs_dir = pathlib.Path("dataset")
    images = list(imgs_dir.glob("*//*.jpg"))

    data = {}
    k = 0
    for img_path in images:
        k = k + 1
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

tile_width= int(input("Width (Diameter) for tiles: (10 is default) "))
tile_height = tile_width


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
    i = reshapeImage(i_path)
    # print("Reshaping done")
    i = cv2.imread("tmp/temp_croped_image.png")
    i = cv2.resize(i, (tile_width, tile_height))
    score(i, img, y0, y1, x0, x1)
    img[y0:y1, x0:x1] = i

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cv2.imwrite("outputs/circle/circle_output.png", img)