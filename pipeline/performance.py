import subprocess
import os
from glob import glob

tex_files = os.listdir('tex')
for tex_file in tex_files:
	subprocess.call('python tex2pdf.py tex/'+tex_file+' pdf')

pdf_files = os.listdir('pdf')
for pdf_file in pdf_files:
	if os.path.splitext(pdf_file)[1] == ".pdf":
		csv_file = os.path.splitext(pdf_file)[0] +'.csv'
		subprocess.call('python pdf2csv.py pdf/'+pdf_file+' csv/'+csv_file)	

actual_number = len(list(filter(lambda x: os.path.splitext(x)[1] == ".tex", os.listdir("pdf"))))
found_number = len(list(filter(lambda x: os.stat("csv/"+x).st_size > 0, os.listdir("csv"))))

print(str(found_number) + '/' + str(actual_number))