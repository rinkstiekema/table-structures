import requests
import base64
import json
import sys 
import os

if(len(sys.argv) != 3):
	print("Needs 2 arguments: <input_folder> <output_folder>")
	exit()

if not os.path.exists(os.path.dirname(sys.argv[1])):
	print("Path input_folder not a folder")
	exit()

if not os.path.exists(os.path.dirname(sys.argv[2])):
	print("Path output_folder not a folder")
	exit()

input_folder = sys.argv[1]
output_folder = sys.argv[2]
input_files = os.listdir(input_folder)

progress_count = 0
for input_file_name in input_files:
	print(str(progress_count)+"%\t | Processing: "+input_file_name)
	with open(os.path.join(input_folder,input_file_name), "rb") as image_file:
		r = requests.post("https://api.ocr.space/parse/image", data={"apikey": "dfcec6347388957", "isTable": "true"}, files={"base64Image":image_file})
		output_file_name = os.path.splitext(input_file_name)[0] + ".tsv"
		with open(os.path.join(output_folder, output_file_name), "w") as output_file:
			text = json.loads(r.text)['ParsedResults'][0]['ParsedText']
			output_file.write(text)
			output_file.close()
	progress_count += 100/len(input_files)