import os
import numpy as np
import pandas as pd
import json

def json2csv(json_folder, csv_folder):
    for json_file in os.listdir(json_folder):
        json_location = os.path.join(json_folder, json_file)
        with open(json_location, 'r+') as jfile:
            tables = json.load(jfile)
            
            for table in tables:
                # Unique occurences of rows and columns
                rows = list(set([x["rect"][0][1] for x in table["cells"]]))
                columns = list(set([x["rect"][0][0] for x in table["cells"]]))

                # Replace row/col by their index
                index_rows = list(set(sorted([cell["rect"][0][1] for cell in table["cells"]])))
                index_columns = list(set(sorted([cell["rect"][0][0] for cell in table["cells"]])))

                matrix = [['' for _ in range(len(rows))] for _ in range(len(columns))]
                for cell in table["cells"]:
                    x = index_rows.index(cell["rect"][0][1])
                    y = index_columns.index(cell["rect"][0][0])
                    matrix[x][y] = cell["words"]

                df = pd.DataFrame(matrix)

                csv_name = os.path.splitext(os.path.basename(table["renderURL"]))[0] + ".csv"
                df.to_csv(os.path.join(csv_folder, csv_name), index=False, header=False)





