import os
import numpy as np
import pandas as pd
import json
import utils
from tqdm import tqdm

def json2csv(json_folder, csv_folder):
    for json_file in os.listdir(json_folder):
        try:
            json_location = os.path.join(json_folder, json_file)
            with open(json_location, 'r+', encoding=utils.get_encoding_type(json_location), errors='ignore') as jfile:
                tables = json.load(jfile)
                
                for table in tables:
                    # Unique occurences of rows and columns
                    rows = list(set([x["rect"][0][1] for x in table["cells"]]))
                    columns = list(set([x["rect"][0][0] for x in table["cells"]]))
                    # Replace row/col by their index
                    index_rows = sorted(list(set([cell["rect"][0][1] for cell in table["cells"]])))
                    index_columns = sorted(list(set([cell["rect"][0][0] for cell in table["cells"]])))

                    matrix = [['' for _ in range(len(columns))] for _ in range(len(rows))]
                    for cell in table["cells"]:
                        x = index_rows.index(cell["rect"][0][1])
                        y = index_columns.index(cell["rect"][0][0])
                        matrix[x][y] = cell["words"]
                        
                    df = pd.DataFrame(matrix)

                    # drop completely empty rows and columns
                    df = df.replace('', np.nan)
                    df = df.dropna(how='all', axis=0)
                    df = df.dropna(how='all', axis=1)
                    df.to_csv(os.path.join(csv_folder, table["name"]+'.csv'), index=False, header=False)
        except Exception as e:
            print(e)
            continue




