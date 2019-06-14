from tabulaOptions import Options
import os
import sys
import subprocess 
from tabula import read_pdf
import json
import textboxtract
from tqdm import tqdm

def init_folders(base_folder, mode):
    pdf_folder = os.path.join(base_folder, "pdf", mode)
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    json_folder = os.path.join(base_folder, "json", mode)
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    png_folder = os.path.join(base_folder, "png", mode)
    if not os.path.exists(png_folder):
        os.makedirs(png_folder)

    results_folder = os.path.join(base_folder, "csv_tabula", mode)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    return pdf_folder, json_folder, png_folder, results_folder

if __name__ == '__main__':
    opt = Options().parse()
    pdf_folder, json_folder, png_folder, results_folder = init_folders(opt.dataroot, opt.mode)

    # for pdf in tqdm(os.listdir(pdf_folder)):
    #     region_boundary = textboxtract.get_region_boundary(os.path.join(pdf_folder, pdf))
    #     data = [{
    #         "name": os.path.splitext(pdf)[0].split("-")[-1],
    #         "page": 1,
    #         "dpi": 150,
    #         "regionBoundary": region_boundary,
    #         "renderURL": os.path.join(png_folder, os.path.splitext(pdf)[0] + '.png')
    #     }]
    #     with open(os.path.join(json_folder, os.path.splitext(pdf)[0]+'.json'), 'w') as outfile:
    #         json.dump(data, outfile)

	# Create CSV files from the extracted text and locations of said text
    if not opt.skip_create_csv:
        for json_file_name in tqdm(os.listdir(json_folder)):
            print(json_file_name)
            json_path = os.path.join(json_folder, json_file_name)
            pdf_path = os.path.join(pdf_folder, os.path.splitext(json_file_name)[0]+'.pdf')

            with open(json_path) as jfile:
                json_data = json.load(jfile)
                for table in json_data:
                    area = table["regionBoundary"]
                    area = [area["x1"], area["y1"], area["x2"], area["y2"]]
                    try:            
                        df = read_pdf(pdf_path, pages=table["page"], silent=True, pandas_options={'index_col': [0]})
                        if df is not None and not df.empty:
                            df.to_csv(os.path.join(results_folder, os.path.splitext(json_file_name)[0]+'.csv'))
                    except Exception as e:
                        print("skipping.. %s"%e)
                        continue
