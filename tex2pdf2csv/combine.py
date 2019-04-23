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

def combine_images(location):
	images_list = os.listdir(location)
	count = 0
	for image in images_list:
		try:
			base_name = "-".join(".".join(image.split(".")[0:-1]).split("-")[0:-1])
			#print(image, location+base_name+"-A.png")
			img_A = Image.open(location+base_name+"-A.png")
			img_B = Image.open(location+base_name+"-B.png")

			old_size = img_A.size
			new_size = img_B.size
			new_A = Image.new("RGB", new_size, color="white") 
			new_A.paste(img_A, (int((new_size[0]-old_size[0])/2),
		        	              int((new_size[1]-old_size[1])/2)))

			new_B = Image.new("RGB", new_size, color="white")
			new_B.paste(img_B, (0,0))

			combined = np.hstack((np.array(new_A), np.array(new_B)))
			scipy.misc.imsave(location+base_name+".png", combined)
			count += 1
			if(count % 100 == 0):
				print(count, " out of ", len(images_list), " combined")
		except:
			continue

def combine(location):
	combine_images(location)
	clean_up(location)
