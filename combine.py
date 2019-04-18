import numpy as np
import scipy.misc
import os

def imread(path, is_grayscale = False):
    if (is_grayscale):
        return scipy.misc.imread(path, flatten = True).astype(np.float)
    else:
        return scipy.misc.imread(path).astype(np.float)

def combine_images(location):
	images_list = os.listdir(location+"A")
	for image in images_list:
		base_name = "-".join(".".join(image.split(".")[0:-1]).split("-")[0:-1])
		img_A = imread(location+"A/"+base_name+"-noborders.png")
		img_B = imread(location+"B/"+base_name+"-borders.png")
		combined = np.hstack((img_A, img_B))
		scipy.misc.imsave(location+base_name+".png", combined)

locations = ["../data/png/train/", "../data/png/test/"]

for location in locations:
	combine_images(location)