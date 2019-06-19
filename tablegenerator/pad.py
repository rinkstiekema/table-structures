import numpy as np
import os
import sys
import imageio

def pad(a, img_res):
	"""Return bottom right padding."""
	zeros = np.full(img_res, 255)
	zeros[:a.shape[0], :a.shape[1], :a.shape[2]] = a
	return zeros

def pad_image(location1, location2, res):
    resolution = (res, res, 3)
    img1 = imageio.imread(location1, mode='RGB').astype(np.float)
    img2 = imageio.imread(location2, mode='RGB').astype(np.float)

    if((img1.shape[0] <= res and img1.shape[1] <= res) or (img2.shape[0] <= res and img2.shape[1] <= res)):
        padded = pad(img1, resolution)
        imageio.imsave(location1, padded)
        padded = pad(img2, resolution)
        imageio.imsave(location2, padded)
    else:
        os.remove(location1)
        os.remove(location2)