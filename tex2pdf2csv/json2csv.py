import os
import sys
import json
import tabula

def json2csv(json_file, pdf_file, csv_file):
	if not os.path.exists("csv"):
		os.makedirs("csv")

	with open(json_file) as jfile:
		print("Converting "+json_file)
		data = json.load(jfile)
		for idx, table in enumerate(data):
			if(table["figType"] == "Table"):
				regionBoundary = table['regionBoundary']
				bbox = [regionBoundary['y1'], regionBoundary['x1'], regionBoundary['y2'], regionBoundary['x2']]
				csv_file_idx = os.path.splitext(csv_file)[0] + "-" + str(idx) + ".csv"
				tabula.convert_into(pdf_file, csv_file_idx, output_format="csv", silent=True, page=table["page"], area=bbox)
