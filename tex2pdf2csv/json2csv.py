import os
import sys
import json
import tabula

def json2csv(json_file, pdf_file, csv_file):
	if not os.path.exists("csv"):
		os.makedirs("csv")

	with open(json_file) as jfile:
		data = json.load(jfile)
		for idx, table in enumerate(data):
			regionBoundary = table['regionBoundary']
			bbox = [regionBoundary['y1'], regionBoundary['x1'], regionBoundary['y2'], regionBoundary['x2']]
			csv_file = os.path.splitext(csv_file)[0] + "-" + str(idx) + ".csv"
			tabula.convert_into(pdf_file, csv_file, output_format="csv", silent=True, area=bbox)