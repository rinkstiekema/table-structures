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
import json2csv

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
	
	csv_folder = os.path.join(base_folder, "csv")
	if not os.path.exists(csv_folder):
		os.makedirs(csv_folder)
	
	return pdf_folder, json_folder, png_folder, outlines_folder, csv_folder

if __name__ == '__main__':
	opt = Options().parse()
	pdf_folder, json_folder, png_folder, outlines_folder, csv_folder = init_folders(opt.dataroot)

	if not opt.skip_generate_images:
		print("Generating images")
		os.system('java -jar pdffigures2.jar -i 72 -e -q -a Table -m ' + png_folder + '\ -d ' + json_folder + '\ ' + pdf_folder + '"')
		for image in os.listdir(png_folder):
			# to do remove from json file
			img = scipy.misc.imread(os.path.join(png_folder, image), mode='RGB').astype(np.float)
			if img.shape[0] > 1024 or img.shape[1] > 1024:
				os.remove(os.path.join(png_folder, image))
				continue
			img = combine.pad(img, (1024, 1024, 3))
			scipy.misc.imsave(os.path.join(png_folder, image), img)

	# Process the tables, add outline URL to respective JSON file
	if not opt.skip_predict:
		print("Predicting outlines")
		os.system('cd pix2pixHD; ./scripts/predict.sh %s' % outlines_folder)

	# Interpret ruling lines and write individual cells to json file
	if not opt.skip_find_cells:
		print("Finding cells")
		rulers.rule(json_folder)

	# Extract the text, using the bounding boxes, from the original PDF
	if not opt.skip_extract_text:
		print("Extracting text")
		textboxtract.extract(json_folder, pdf_folder)

	# Create CSV files from the extracted text and locations of said text
	if not opt.skip_create_csv:
		print("Creating csv")
		json2csv.json2csv(json_folder, csv_folder)