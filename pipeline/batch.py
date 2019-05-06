from options import Options
import numpy as np
import json
import os
import sys
import subprocess 
import predictor
import combine
import rulers 
import scipy.misc
import textboxtract

def init_folders(base_folder):
	pdf_folder = os.path.join(base_folder, "pdf")
	if not os.path.isdir(pdf_folder):
		print(pdf_folder+" is not a directory")
		exit(-1)

	json_folder = os.path.join(base_folder, "json")
	if not os.path.exists(json_folder):
		os.makedirs(json_folder)

	png_folder = os.path.join(base_folder, "png")
	if not os.path.exists(png_folder):
		os.makedirs(png_folder)

	outlines_folder = os.path.join(base_folder, "outlines")
	if not os.path.exists(outlines_folder):
		os.makedirs(outlines_folder)

	return pdf_folder, json_folder, png_folder, outlines_folder

if __name__ == '__main__':
	if not os.path.exists("pdffigures2"):
		print("pdffigures2 is not available in this folder")
		exit(-1)

	opt = Options().parse()
	pdf_folder, json_folder, png_folder, outlines_folder = init_folders(opt.dataroot)

	if(opt.generate_images):
		os.system('java -jar pdffigures2.jar -e -q -a Table -m ' + png_folder + '\ -d ' + json_folder + '\ ' + pdf_folder + '"')
		for image in os.listdir(png_folder):
			# to do remove from json file
			img = scipy.misc.imread(os.path.join(png_folder, image), mode='RGB').astype(np.float)
			if img.shape[0] > 1024 or img.shape[1] > 1024:
				os.remove(os.path.join(png_folder, image))
				continue
			img = combine.pad(img, (1024, 1024, 3))
			scipy.misc.imsave(os.path.join(png_folder, image), img)

	# Process the tables, add outline URL to respective JSON file
	#predictor.predict(json_folder, outlines_folder)

	rulers.rule(json_folder)	
	textboxtract.extract(json_folder)