import os
import sys
import json

def json2png(root, file_name):
	png_folder = os.path.join(root, "../png")
	
	json_file = os.path.join(root, 'json', file_name)
	if not os.path.exists(png_folder):
		os.makedirs(png_folder)

	with open(json_file) as jfile:
		print("Converting "+file_name)
		data = json.load(jfile)
		for idx, table in enumerate(data):
			if(table["figType"] == "Table"):
				regionBoundary = table['regionBoundary']
				bbox = [regionBoundary['y1'], regionBoundary['x1'], regionBoundary['y2'], regionBoundary['x2']]
				csv_file_idx = os.path.splitext(csv_file)[0] + "-" + str(idx) + ".csv"
				tabula.convert_into(pdf_file, csv_file_idx, output_format="csv", silent=True, page=table["page"], area=bbox)
