import numpy as np
import os
import sys
import scipy.misc

def pad(a, img_res):
	"""Return bottom right padding."""
	zeros = np.full(img_res, 255)
	zeros[:a.shape[0], :a.shape[1], :a.shape[2]] = a
	return zeros

if len(sys.argv) < 2:
    print("Missing arguments. Usage: <input-folder> <resolution>")    
    exit(-1)

folder = sys.argv[1]
resolution = (int(sys.argv[2]), int(sys.argv[2]), 3)
for image in os.listdir(folder):
    print(image)
    location = os.path.join(folder, image)
    padded = pad(scipy.misc.imread(location, mode='RGB').astype(np.float), resolution)
    scipy.misc.imsave(location, padded)
