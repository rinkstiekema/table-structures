import tabula
import sys
import os

if(len(sys.argv) < 2):
	print("Missing arguments: usage <pdf file> <output file>")

pdf_file = sys.argv[1]
csv_file = sys.argv[2]

tabula.convert_into(pdf_file, csv_file, output_format="csv")


# df = tabula.read_pdf("test.pdf", options)
# print(df)