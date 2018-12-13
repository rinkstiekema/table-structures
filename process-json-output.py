import os
import json

for file in os.listdir("../data/output-json/"):
	with open(os.path.join("../data/output-json/", file)) as jsonFile:
		file_list = json.loads(jsonFile.read())
		filtered_list = [i['renderURL'] for i in file_list if i['figType'] != 'Table']

		for i in filtered_list:
			os.remove(i)
	

