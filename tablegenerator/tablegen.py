import sys
import os
import json
import subprocess
import string 
import numpy as np
from functools import partial
from multiprocessing import Pool
from pad import pad_image
from texgen import TexGenerator
from random import randrange, randint, getrandbits, choice, sample
from table import Table
from pprint import pprint
import argparse
import textboxtract

class TableGenerator():
    def __init__(self, table_type):
        self.table_type = table_type

    def randBoolean(self, percent):
        return randrange(100) < percent

    def generate(self):
        n_rows = randint(2, 15)
        n_columns = randint(2, 8)
        n_text_columns = 0 if self.randBoolean(80) else randint(1, n_columns)
        return Table(self.table_type, n_rows, n_columns, n_text_columns)

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def cleanup(dir_name, extension):
    dir_list = os.listdir(dir_name)

    for item in dir_list:
        if not item.endswith(extension):
            filename = os.path.join(dir_name, item)
            if not os.path.isdir(filename):
                os.remove(filename)

def get_amount(path):
    if path[0] == 'train':
        return 1100
    else:
        return 550

def generate(idx, table_type, paths, csv_path, png_path, tex_path, pdf_path, aux_path, args):
    tex_generator = TexGenerator()
    table_generator = TableGenerator(table_type)
    for path in np.array(paths).reshape(-1, 2):
        n = get_amount(path)
        for i in range(n):
            table = table_generator.generate()
            csv = table.df.to_csv(index=table.n_stubs > 0, header=table.n_headers > 0).replace(" \\\\ ", " ").replace("\\makecell{", "").replace("}", "").replace("\n", "")
            
            with open(os.path.join(csv_path, path[0] ,str(idx))+'-'+str(i)+'.csv', 'w+') as csv_file:
                csv_file.write(csv)
            
            table_tex = tex_generator.generate_tex(table)
            outline_tex = tex_generator.generate_tex_outline(table)

            with open(os.path.join(tex_path, path[0],str(idx))+'-'+str(i)+'.tex', 'w+') as tex_file:
                tex_file.write(table_tex)

            subprocess.call('pdflatex -quiet -output-directory '+os.path.join(pdf_path, path[0])+' '+os.path.join(tex_path, path[0], str(idx)+'-'+str(i)) + '.tex')

            subprocess.call('latex -interaction=batchmode -output-directory='+ os.path.join(png_path, path[0]) + ' ' + os.path.join(tex_path, path[0], str(idx)+'-'+str(i)) + '.tex', shell=True, stdout=open(os.devnull, 'wb'))
            subprocess.call('dvipng -q* -T tight -o ' + os.path.join(png_path, path[0], str(idx)+'-'+str(i)) + '.png ' + os.path.join(png_path, path[0], str(idx)+'-'+str(i)) + '.dvi', shell=True, stdout=open(os.devnull, 'wb'))
            
            with open(os.path.join(tex_path, path[1],str(idx))+'-'+str(i)+'.tex', 'w+') as tex_file:
                tex_file.write(outline_tex)
            subprocess.call('latex -interaction=batchmode -output-directory='+ os.path.join(png_path, path[1]) + ' ' + os.path.join(tex_path, path[1], str(idx)+'-'+str(i)) + '.tex', shell=True, stdout=open(os.devnull, 'wb'))
            subprocess.call('dvipng -q* -T tight -o ' + os.path.join(png_path, path[1], str(idx)+'-'+str(i)) + '.png ' + os.path.join(png_path, path[1], str(idx)+'-'+str(i)) + '.dvi', shell=True, stdout=open(os.devnull, 'wb'))

            if args.padding:
                try:
                    pad_image(os.path.join(png_path, path[0], str(idx)+'-'+str(i)) + '.png', os.path.join(png_path, path[1], str(idx)+'-'+str(i)) + '.png', args.resolution)
                except:
                    os.remove(os.path.join(png_path, path[0], str(idx)+'-'+str(i)) + '.png')
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--location', type=str, help='Path to save the dataset to.')
    parser.add_argument('--padding', type=bool, default=False, help='Pad images')
    parser.add_argument('--resolution', type=int, default=1024, help='Resolution to pad images to')
    args = parser.parse_args()
    
    location = args.location

    csv_path = os.path.join(location, 'csv')
    make_dir(csv_path)
    
    tex_path = os.path.join(location, 'tex')
    make_dir(tex_path)

    png_path = os.path.join(location, 'png')
    make_dir(png_path)

    pdf_path = os.path.join(location, 'pdf')
    make_dir(pdf_path)

    json_path = os.path.join(location, 'json')
    make_dir(json_path)

    paths = ['val', 'val_labels'] #['train', 'train_labels', 'val', 'val_labels', 'test', 'test_labels']
    for idx, path in enumerate(paths):
        new_path_tex = os.path.join(tex_path, path)
        make_dir(new_path_tex)
        new_path_png = os.path.join(png_path, path)
        make_dir(new_path_png)
        if idx % 2 == 0:
            new_path_csv = os.path.join(csv_path, path)
            make_dir(new_path_csv)
            new_path_pdf = os.path.join(pdf_path, path)
            make_dir(new_path_pdf)
            new_path_json = os.path.join(json_path, path)
            make_dir(new_path_json)
    aux_path = os.path.join(location, 'aux-data')
    make_dir(aux_path)

    with open('tabletypes.json') as data_file:    
        types = json.load(data_file)

    # for idx, i in enumerate(types):
    #     generate(idx, paths=paths, csv_path=csv_path, png_path=png_path, tex_path=tex_path, pdf_path=pdf_path, aux_path=aux_path, args=args, table_type=i)

    pool = Pool()
    pool.starmap(partial(generate, paths=paths, csv_path=csv_path, png_path=png_path, tex_path=tex_path, pdf_path=pdf_path, aux_path=aux_path, args=args), list(enumerate(types)))

    for path in np.array(paths).reshape(-1, 2):
        cleanup(os.path.join(png_path, path[0]), '.png')
        cleanup(os.path.join(png_path, path[1]), '.png')
        cleanup(os.path.join(pdf_path, path[0]), '.pdf')

    for idx, path in enumerate(paths):
        if idx % 2 == 0:
            for pdf in os.listdir(os.path.join(pdf_path, path)):
                region_boundary = textboxtract.get_region_boundary(os.path.join(pdf_folder, path, pdf))
                data = [{
                    "name": os.path.splitext(pdf)[0],
                    "page": 1,
                    "dpi": 150,
                    "regionBoundary": region_boundary
                }]
                with open(os.path.join(json_folder, path, os.path.splitext(pdf)[0]+'.json'), 'w') as outfile:
                    json.dump(data, outfile)
