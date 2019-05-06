from operator import itemgetter 
from itertools import groupby
import os
import json
import fitz
import sys

def texboxtract(pdf, tables):
    for table in tables:
        doc = fitz.open(pdf)
        page = doc[int(table["page"])]
        words = page.getTextWords()
        for cell in table["cells"]:
            rect = [cell[0][0]+table["regionBoundary"]["x1"], cell[0][1]+table["regionBoundary"]["y1"], cell[1][0]+table["regionBoundary"]["x1"], cell[1][1]+table["regionBoundary"]["y1"]]
            
            mywords = [w for w in words if fitz.Rect(w[:4])in fitz.Rect(rect)]
            mywords.sort(key = itemgetter(3, 0))   # sort by y1, x0 of the word rect
            group = groupby(mywords, key = itemgetter(3))
            
            result = ""
            for y1, gwords in group:
                result += " ".join(w[4] for w in gwords)
            cell = {rect: [(rect[0], rect[1]), (rect[2], rect[3])], words: result}
    return tables

def extract(json_folder, pdf_folder):
	for json_file in os.listdir(json_folder):
		json_file_location = os.path.join(json_folder, json_file)
		with open(json_file_location, 'r+') as jfile:
			print("Starting on extracting text from: "+json_file_location)
			tables = json.load(jfile)
			filename, file_extension  = os.path.splitext(os.path.basename(json_file_location))
			pdf_location = os.path.join(pdf_folder, filename, ".pdf")
			tables = texboxtract(pdf_location, tables)

			jfile.seek(0)
			jfile.write(json.dumps(tables))
			jfile.truncate()