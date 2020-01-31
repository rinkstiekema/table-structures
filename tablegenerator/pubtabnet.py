import json
from collections import defaultdict
import os

def combine_tokens_structure(cells, structure):
    result = ""
    for tag in structure:
        result += tag
        if '<td' in tag:
            result += ''.join(cells.pop(0)['tokens'])

with open('pubtabnet.json') as fPubTabNet:
    while line in fptn:
        table_json = json.load(line)

        filename_meta = table_json['filename'].split('_')
        filename = filename_meta[0]
        page = filename_meta[1]
        table_n = filename_meta[2].split('.')[0]

        cells = table_json['html']['cells']
        structure = table_json['html']['structure']

        table = combine_tokens_structure(cells, structure)
      
            
                

            


            