from options import Options
import numpy as np
import json
import os
import sys
import subprocess 
import pad
import rulers 
import scipy.misc
import textboxtract
import json2csv
from tqdm import tqdm
# from segmentation.predict import predict

def init_folders(base_folder):
	pdf_folder = os.path.join(base_folder, "pdf")
	if not os.path.exists(pdf_folder):
		os.makedirs(pdf_folder)

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

def add_outline_url(json_folder, outline_folder):
	for json_file in os.listdir(json_folder):
		json_file_location = os.path.join(json_folder, json_file)
		with open(json_file_location, 'r+') as jfile:
			result = [] # eventually new json file
			tables = json.load(jfile) # current json file
			for table in tables:
				table["outlineURL"] = os.path.join(outline_folder, os.path.basename(table["renderURL"]))
				result.append(table)
			jfile.seek(0)
			jfile.write(json.dumps(result))
			jfile.truncate()

if __name__ == '__main__':
	opt = Options().parse()
	pdf_folder, json_folder, png_folder, outlines_folder, csv_folder = init_folders(opt.dataroot)

    for pdf in pdf_folder:
        region_boundary = textboxtract.get_region_boundary(os.path.join(pdf_folder, pdf))
        data = [{
            "name": os.path.splitext(pdf)[0].split("-")[-1],
            "page": 1,
            "dpi": 150,
            "regionBoundary": region_boundary,
            "renderURL": os.path.join(png_folder, os.path.splitext(pdf)[0] + '.png')
        }]
        json.dump(os.path.join(json_folder, os.path.splitext(pdf)[0]+'.json'))

	# Process the tables, add outline URL to respective JSON file
	if not opt.skip_predict:
		print("Predicting outlines")
		if opt.model == 'pix2pix':
			subprocess.call('sh ./pixpred.sh %s %s %s %s' % ('gen-tables', opt.checkpoint_dir, opt.dataroot, outlines_folder))
		else:
			subprocess.call('sh ./segpred.sh %s %s %s %s' % ('gen-tables', opt.checkpoint_dir, opt.dataroot, outlines_folder))
	add_outline_url(json_folder, outlines_folder)

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
		json2csv.json2csv(json_folder, opt.resultsroot)