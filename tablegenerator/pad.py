import numpy as np
import os
import sys
import scipy.misc

def pad(a, img_res):
	"""Return bottom right padding."""
	zeros = np.full(img_res, 255)
	zeros[:a.shape[0], :a.shape[1], :a.shape[2]] = a
	return zeros

def pad_image(location, res):
    resolution = (res, res, 3)
    img = scipy.misc.imread(location, mode='RGB').astype(np.float)
    if(img.shape[0] <= res and img.shape[1] <= res):
        padded = pad(img, resolution)
        scipy.misc.imsave(location, padded)
    else:
        os.remove(location)

# if len(sys.argv) < 2:
#     print("Missing arguments. Usage: <input-folder> <resolution>")    
#     exit(-1)

# folder = sys.argv[1]
# resolution = (int(sys.argv[2]), int(sys.argv[2]), 3)
# for image in os.listdir(folder):
#     location = os.path.join(folder, image)
#     img = scipy.misc.imread(location, mode='RGB').astype(np.float)
#     if(img.shape[0] <= 1024 and img.shape[1] <= 1024):
#         padded = pad(img, resolution)
#         scipy.misc.imsave(location, padded)
#     else:
#         os.remove(location)
