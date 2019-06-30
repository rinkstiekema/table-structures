from tabulaOptions import Options
import os
import sys
import subprocess 
from tabula import read_pdf
import json
import textboxtract
from tqdm import tqdm

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

    results_folder = os.path.join(base_folder, "csv_tabula")
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    return pdf_folder, json_folder, png_folder, results_folder

if __name__ == '__main__':
    opt = Options().parse()
    pdf_folder, json_folder, png_folder, results_folder = init_folders(opt.dataroot)

    if not opt.skip_generate_images:
        print("Generating images")
        os.system('java -jar pdffigures2.jar -e -q -a Table -m ' + png_folder + '/ -d ' + json_folder + '/ ' + pdf_folder + '/')

	# Create CSV files from the extracted text and locations of said text
    if not opt.skip_create_csv:
        for json_file_name in tqdm(os.listdir(json_folder)[22:]):
            json_path = os.path.join(json_folder, json_file_name)
            pdf_path = os.path.join(pdf_folder, os.path.splitext(json_file_name)[0]+'.pdf')

            with open(json_path) as jfile:
                json_data = json.load(jfile)
                basename = os.path.splitext(os.path.basename(json_path))[0]
                for table in json_data:
                    area = table["regionBoundary"]
                    area = [area["y1"], area["x1"], area["y2"], area["x2"]]
                    try:            
                        df = read_pdf(pdf_path, pages=table["page"]+1,encoding='ISO-8859-1', area=area, guess=False, silent=True)
                        if df is not None and not df.empty:
                            df.to_csv(os.path.join(results_folder, basename+"-Table"+table["name"]+'-1.csv'))
                    except Exception as e:
                        print("skipping.. %s"%e)
                        continue
