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
import imageio
import utils
from tqdm import tqdm
from bs4 import UnicodeDammit

def remove_from_json(json_folder, name):
	base_name = os.path.splitext(name)[0]
	with open(os.path.join(json_folder, base_name.split("-")[0]+".json")) as jfile:
		tables = json.load(jfile)
		tables = list(filter(lambda table: not table['name'] == base_name.split("-")[-1], tables))
		jfile.seek(0)
		jfile.write(json.dumps(tables))
		jfile.truncate()

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

if __name__ == '__main__':
	opt = Options().parse()
	pdf_folder, json_folder, png_folder, outlines_folder, results_folder = init_folders(opt.dataroot, opt.model)

	if not opt.skip_generate_images:
		print("Generating images")
		os.system('java -jar pdffigures2.jar -e -q -a Table -m ' + png_folder + '/ -d ' + json_folder + '/ ' + pdf_folder + '/')
		print("Padding images")
		for image in tqdm(os.listdir(png_folder)):
			img = np.asarray(imageio.imread(os.path.join(png_folder, image), pilmode='RGB'), dtype=np.uint8)
			if img.shape[0] > 1024 or img.shape[1] > 1024:
				os.remove(os.path.join(png_folder, image))
				remove_from_json(json_folder, image)
				continue
			img = pad.pad(img, (1024, 1024, 3))
			imageio.imwrite(os.path.join(png_folder, image), img)				

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
					basename = os.path.splitext(paper)[0] + '-Table' + table["name"] + '-1'
					table = rulers.rule(table, opt)
					pdf_location = os.path.join(pdf_folder, basename.split("-")[0]+'.pdf')
					table = textboxtract.texboxtract(pdf_location, table)
					
					csv = json2csv.json2csv(table)
					csv_location = os.path.join(results_folder, basename+'.csv')
					with open(csv_location, 'w', encoding='utf-8') as csv_file:
						csv_file.write(csv)
				except Exception as e:
					print(e)
					continue
	print("Finished")