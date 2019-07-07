from options import Options
import numpy as np
import json
import os
import sys
import subprocess 
import pad
import rulers 
import textboxtract
import json2csv
import utils
from tqdm import tqdm

def init_folders(base_folder, model):
	pdf_folder = os.path.join(base_folder, "pdf")
	if not os.path.exists(pdf_folder):
		os.makedirs(pdf_folder)

	json_folder = os.path.join(base_folder, "json")
	if not os.path.exists(json_folder):
		os.makedirs(json_folder)

	png_folder = os.path.join(base_folder, "png")
	if not os.path.exists(png_folder):
		os.makedirs(png_folder)

	outlines_folder = os.path.join(base_folder, "outlines_"+model)
	if not os.path.exists(outlines_folder):
		os.makedirs(outlines_folder)

	results_folder = os.path.join(base_folder, "csv_pred_"+model)
	if not os.path.exists(results_folder):
		os.makedirs(results_folder)

	return pdf_folder, json_folder, png_folder, outlines_folder, results_folder

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
	pdf_folder, json_folder, png_folder, outlines_folder, results_folder = init_folders(opt.dataroot, opt.model)

	# Process the tables, add outline URL to respective JSON file
	if not opt.skip_predict:
		print("Predicting outlines")
		if opt.model == 'pix2pixHD':
			subprocess.call(['python', './pix2pixHD/predict.py', '--name', 'gen-tables', '--checkpoints_dir', opt.checkpoint_dir,  '--dataroot', opt.dataroot, '--loadSize', '1024', '--fineSize', '1024', '--no_instance', '--label_nc', '0', '--results_dir', outlines_folder, '--mode', opt.mode, '--which_epoch', opt.epoch])
		elif opt.model == 'encoder-decoder-skip':
			subprocess.call(['python', './segmentation/bulk_predict.py', '--input_folder', png_folder, '--output_folder', outlines_folder, '--checkpoint_path', opt.checkpoint_dir, '--crop_height', '1024', '--crop_width', '1024', '--model', 'Encoder-Decoder-Skip'])
		else:
			print("Unknown model")
			exit(-1)

	for paper in tqdm(os.listdir(json_folder)):
		json_file_location = os.path.join(json_folder, paper)
		with open(json_file_location, 'r+', encoding=utils.get_encoding_type(json_file_location), errors='ignore') as jfile:
			tables = json.load(jfile)

			for table in tables:
				try:
					basename = table["name"]
					table = rulers.rule(table, opt)
					pdf_location = os.path.join(pdf_folder, basename.split("-")[0]+'.pdf')
					table = textboxtract.texboxtract_synthetic(pdf_location, table)
					
					csv = json2csv.json2csv(table)
					csv_location = os.path.join(results_folder, basename+'.csv')
					with open(csv_location, 'w', encoding='utf-8') as csv_file:
						csv_file.write(csv)
				except Exception as e:
					print(e)
					continue
	print("Finished")