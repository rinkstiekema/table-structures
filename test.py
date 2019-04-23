import numpy as np
import scipy.misc

def pad(a):
    """Return bottom right padding."""
    zeros = np.full((1024, 1024, 3), 255)
    zeros[:a.shape[0], :a.shape[1], :a.shape[2]] = a
    return zeros

def imread(path):
    return scipy.misc.imread(path, mode='RGB').astype(np.float)

img = imread("../2905-0.png")
img_padded = pad(img)
scipy.misc.imsave("../2905-0-padded.png", img_padded)
