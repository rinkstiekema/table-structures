import os
import sys
import subprocess 
import json2csv

if(len(sys.argv) < 2):
	print("Missing argument. Usage: <pdf folder>")
	exit(-1)

pdf_folder = sys.argv[1]
if not os.path.isdir(pdf_folder):
	print(pdf_folder+" is not a directory")
	exit(-1)

if not os.path.exists("json"):
    os.makedirs("json")

if not os.path.exists("pdffigures2"):
	print("pdffigures2 is not available in this folder")
	exit(-1)

os.system(r'cd pdffigures2 & sbt "run-main org.allenai.pdffigures2.FigureExtractorBatchCli ../' + pdf_folder + ' -s stat_file.json -d ../json/ -a Table "')

json_files = os.listdir("json")

for json_file in json_files:
	csv_file = "csv/" + os.path.splitext(json_file)[0] + ".csv"
	pdf_file = "pdf/" + os.path.splitext(json_file)[0] + ".pdf"
	json2csv.json2csv("json/"+json_file, pdf_file, csv_file)