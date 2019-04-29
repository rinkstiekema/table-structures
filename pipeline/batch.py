import json
import os
import sys
import subprocess 
import predictor
import rulers 
# import textboxtract

if(len(sys.argv) < 2):
	print("Missing argument. Usage: <folder>")
	exit(-1)

folder = sys.argv[1]

pdf_folder = os.path.join(folder, "pdf")
if not os.path.isdir(pdf_folder):
	print(pdf_folder+" is not a directory")
	exit(-1)

json_folder = os.path.join(folder, "json")
if not os.path.exists(json_folder):
    os.makedirs(json_folder)

png_folder = os.path.join(folder, "png")
if not os.path.exists(png_folder):
	os.makedirs(png_folder)

outlines_folder = os.path.join(folder, "outlines")
if not os.path.exists(outlines_folder):
	os.makedirs(outlines_folder)

if not os.path.exists("pdffigures2"):
	print("pdffigures2 is not available in this folder")
	exit(-1)

os.system('cd pdffigures2 & sbt "run-main org.allenai.pdffigures2.FigureExtractorBatchCli -q -a Table -m ' + png_folder + '\ -d ' + json_folder + '\ ' + pdf_folder + '"')

# for json_file in os.listdir(json_folder):
# 	json_file_location = os.path.join(json_folder, json_file)
# 	with open(json_file_location, 'r+') as jfile:
# 		data = json.load(jfile)
# 		tables = []
# 		for idx, table in enumerate(data):
# 			if(table["figType"] == "Table"):
				# tables.append(table)
# 		jfile.seek(0)
# 		jfile.write(json.dumps(tables))
# 		jfile.truncate()

# # Process the tables
# predictor.predict(png_folder, outlines_folder)
# cells = rulers.rule(outlines_folder)

# for json_file in os.listdir(json_folder):
# 	json_file_location = os.path.join(json_folder, json_file)
# 	with open(json_file_location, 'r+') as jfile:
# 		print("Starting on "+json_file_location)
# 		data = json.load(jfile)
# 		tables = []
# 		for idx, table in enumerate(data):
# 			file_name = os.path.basename(table['renderURL'])
# 			print("Table "+str(idx))
# 			table['cells'] = cells[file_name]
# 			tables.append(table)
# 		filename, file_extension  = os.path.splitext(os.path.basename(json_file_location))
# 		pdf_location = os.path.join(pdf_folder, filename, ".pdf")
# 		tables = textboxtract.texboxtract(pdf_location, tables)

# 		jfile.seek(0)
# 		jfile.write(json.dumps(tables))
# 		jfile.truncate()

		
		
		
