Dataset: https://www.kaggle.com/datasets/yamaerenay/100-images-of-top-50-car-brands

Installation:
$python3 -m pip install --upgrade pip
$python3 -m pip install Pillow
$python3 -m pip install opencv-python
$python3 -m pip install numpy


Run:
$pipenv run python mosaic.py


Description:
    In order to make a photomosaic I used python programming language along with OpenCV, 
    Pillow, and NumPy libraries. I followed the first method described in Assignment file, which
    guides to match the patch images to region of interest of the Big Picture by the average RGB
    color. I created cache.json file, which stands for dictionary of image directory path sorted by 
    different RGB values. I generate this file in the beginning and refer to it after the image 
    segmentation process. In image segmentation, for the rectangular mosaics, the program asks for 
    width and height of the tiles and resizes the big picture to the integer number of tiles. For the 
    circular mosaic, the program asks for the diameter as well, but the tiles are considered as a 
    square. The patch image gets cropped right before being pasted on the region of the interest. 
    After that, it traverses through each pixel of the tile to change black pixels to the original 
    picture’s colors because transparent region of circular png images turn to black, and we do it to 
    enhance the mosaic with the original input image. Finally, the program saves the result image in
    output rectangular/circular folder according to the shape of the mosaics.


Folders:
tmp folder is used to store the cropped images for circle mosaic and cache.json file of directories of input images with average colors.
output folder stores all the output images both circular and rectangular mosaics.
dataset folder is sorted by car brands in subfolders.
    
