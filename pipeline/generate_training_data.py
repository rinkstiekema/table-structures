import os 
import multiprocessing as mp
import sys
import json
import subprocess
import itertools
import shutil
from tex2png import tex2png
from combine import combine
from tablegen import generate_tables

if __name__ == '__main__':
	if len(sys.argv) < 3:
	    print("Missing arguments. Usage: <input-folder> <amount>")
	    exit(-1)

	root_folder = sys.argv[1]
	amount = int(sys.argv[2])

	tex_folder = os.path.join(root_folder, "tex")
	if not os.path.exists(tex_folder):
		os.makedirs(tex_folder)

	image_folder = os.path.join(root_folder, "png")
	if not os.path.exists(image_folder):
		os.makedirs(image_folder)

	aux_folder = os.path.join(image_folder, 'aux-bs')
	if not os.path.exists(aux_folder):
		os.makedirs(aux_folder)

	generate_tables(tex_folder, amount)

	tex_list = os.listdir(tex_folder)
	count = 0
	for tex_file in tex_list:
		tex2png(os.path.join(tex_folder, tex_file), image_folder)
		count += 1
		if count % 100 == 0:
			print(count, " out of ", len(tex_list))
	
	a_location = os.path.join(image_folder, "train_A")
	if not os.path.exists(a_location):
		os.makedirs(a_location)
	b_location = os.path.join(image_folder, "train_B")
	if not os.path.exists(b_location):
		os.makedirs(b_location)

	images = os.listdir(image_folder)
	for img in images:
		if not os.path.isfile(os.path.join(image_folder, img)):
			continue
		if "-A" in img:
			os.rename(os.path.join(image_folder, img), os.path.join(image_folder, "train_A", img.replace("-A", "")))
		else:
			os.rename(os.path.join(image_folder, img), os.path.join(image_folder, "train_B", img.replace("-B", "")))

	shutil.rmtree(aux_folder) 
	# combine(output_folder)

