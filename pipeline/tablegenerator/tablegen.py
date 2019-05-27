import sys
import os
import json
import subprocess
from random import randrange, randint, getrandbits, choice, sample
import string 
import numpy as np
from texgen import TexGenerator
from table import Table
from pprint import pprint

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
        os.mkdir(path)

def cleanup(dir_name):
    dir_list = os.listdir(dir_name)

    for item in dir_list:
        if not item.endswith(".png"):
            filename = os.path.join(dir_name, item)
            if not os.path.isdir(filename):
                os.remove(filename)

def get_amount(path):
    if path[0] == 'train':
        return 1100
    else:
        return 550

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Missing argument. Usage: <location>")
        exit(-1)

    location = sys.argv[1]
    tex_generator = TexGenerator()

    csv_path = os.path.join(location, 'csv')
    make_dir(csv_path)
    
    tex_path = os.path.join(location, 'tex')
    make_dir(tex_path)

    png_path = os.path.join(location, 'png')
    make_dir(png_path)

    paths = ['train', 'train_label', 'val', 'val_label', 'test', 'test_label']
    for idx, path in enumerate(paths):
        new_path_tex = os.path.join(tex_path, path)
        make_dir(new_path_tex)
        new_path_png = os.path.join(png_path, path)
        make_dir(new_path_png)
        if idx % 2 == 0:
            new_path_csv = os.path.join(csv_path, path)
            make_dir(new_path_csv)

    with open('tabletypes.json') as data_file:    
        types = json.load(data_file)

    tex_generator = TexGenerator()
    for idx, table_type in enumerate(types):
        table_generator = TableGenerator(table_type)
        
        for path in np.array(paths).reshape(-1, 2):
            n = get_amount(path)
            for i in range(n):
                if i % 100 == 0:
                    print("%i out of %i" % (i, n))

                table = table_generator.generate()
                csv = table.df.to_csv().replace("\n", "")
                with open(os.path.join(csv_path, path[0] ,str(idx))+'-'+str(i)+'.csv', 'w+') as csv_file:
                    csv_file.write(csv)
                
                table_tex = tex_generator.generate_tex(table)
                outline_tex = tex_generator.generate_tex_outline(table)

                with open(os.path.join(tex_path, path[0],str(idx))+'-'+str(i)+'.tex', 'w+') as tex_file:
                    tex_file.write(table_tex)
                subprocess.call('latex -interaction=batchmode -output-directory='+ os.path.join(png_path, path[0]) + ' ' + os.path.join(tex_path, path[0], str(idx)+'-'+str(i)) + '.tex', shell=True, stdout=open(os.devnull, 'wb'))
                subprocess.call('dvipng -q* -T tight -o ' + os.path.join(png_path, path[0], str(idx)+'-'+str(i)) + '.png ' + os.path.join(png_path, path[0], str(idx)+'-'+str(i)) + '.dvi', shell=True, stdout=open(os.devnull, 'wb'))
                
                with open(os.path.join(tex_path, path[1],str(idx))+'-'+str(i)+'.tex', 'w+') as tex_file:
                    tex_file.write(outline_tex)
                subprocess.call('latex -interaction=batchmode -output-directory='+ os.path.join(png_path, path[1]) + ' ' + os.path.join(tex_path, path[1], str(idx)+'-'+str(i)) + '.tex', shell=True, stdout=open(os.devnull, 'wb'))
                subprocess.call('dvipng -q* -T tight -o ' + os.path.join(png_path, path[1], str(idx)+'-'+str(i)) + '.png ' + os.path.join(png_path, path[1], str(idx)+'-'+str(i)) + '.dvi', shell=True, stdout=open(os.devnull, 'wb'))

            cleanup(os.path.join(png_path, path[0]))
            cleanup(os.path.join(png_path, path[1]))