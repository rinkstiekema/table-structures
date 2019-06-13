from tabulaOptions import Options
import os
import sys
import subprocess 
from tqdm import tqdm
from tabula import read_pdf
import json

def init_folders(base_folder):
	pdf_folder = os.path.join(base_folder, "pdf")
	if not os.path.exists(pdf_folder):
		os.makedirs(pdf_folder)

	json_folder = os.path.join(base_folder, "json")
	if not os.path.exists(json_folder):
		os.makedirs(json_folder)

	png_folder = os.path.join(base_folder, "png")
	if not os.path.exists(png_folder):
		os.makedirs(png_folder)

	return pdf_folder, json_folder, png_folder, csv_folder

if __name__ == '__main__':
    opt = Options().parse()
    pdf_folder, json_folder, png_folder = init_folders(opt.dataroot)

    if not opt.skip_generate_images:
        print("Generating images into %s"%pdf_folder)
        os.system('java -jar pdffigures2.jar -e -q -a Table -m ' + png_folder + '/ -d ' + json_folder + '/ ' + pdf_folder + '/')

	# Create CSV files from the extracted text and locations of said text
    if not opt.skip_create_csv:
        for json_file_name in os.listdir(json_folder):
            json_path = os.path.join(json_folder, json_file_name)
            pdf_path = os.path.join(pdf_folder, os.path.splitext(json_file_name)[0]+'.pdf')

            with open(json_path) as jfile:
                json_data = json.load(jfile)
                for table in json_data:
                    area = table["regionBoundary"]
                    area = [area["x1"], area["y1"], area["x2"], area["y2"]]
                    try:            
                        df = read_pdf(pdf_path, pages=table["page"]+1, area=area, silent=True)
                        if df is not None and not df.empty:
                            df.loc[:, ~df.columns.str.match('Unnamed')]
                            df.to_csv(os.path.join(opt.resultfolder, os.path.splitext(json_file_name)[0]+"-"+table["name"]+'.csv'))
                    except Exception as e:
                        print("skipping.. %s"%e)
                        continue
