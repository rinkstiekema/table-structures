import numpy as np
import scipy.misc
import os
from PIL import Image

def clean_up(location):
	images_list = os.listdir(location)
	for image in images_list:
		try:
			if image.endswith("-A.png") or image.endswith("-B.png"):
				os.remove(os.path.join(location, image))
		except:
			continue

def imread(path, is_grayscale = False):
    if (is_grayscale):
        return scipy.misc.imread(path, flatten = True).astype(np.float)
    else:
        return scipy.misc.imread(path).astype(np.float)

def pad(a):
	"""Return bottom right padding."""
	zeros = np.full(self.img_res, 255)
	zeros[:a.shape[0], :a.shape[1], :a.shape[2]] = a
	return zeros

def combine_images(location):
	images_list = os.listdir(location)
	count = 0
	for image in images_list:
		try:
			base_name = "-".join(".".join(image.split(".")[0:-1]).split("-")[0:-1])
			#print(image, location+base_name+"-A.png")
			# img_A = Image.open(location+base_name+"-A.png")
			# img_B = Image.open(location+base_name+"-B.png")
			img_A = scipy.misc.imread(location+base_name+"-A.png", mode='RGB').astype(np.float)
			img_B = scipy.misc.imread(location+base_name+"-B.png", mode='RGB').astype(np.float) 
			
			img_A = pad(img_A)
			img_B = pad(img_B)

			old_size = img_A.size
			new_size = img_B.size
			combined = np.hstack((np.array(new_A), np.array(new_B)))
			scipy.misc.imsave(location+base_name+".png", combined)
			count += 1
			if(count % 100 == 0):
				print(count, " out of ", len(images_list), " combined")
		except:
			continue

def combine(location):
	combine_images(location)
	# clean_up(location)
