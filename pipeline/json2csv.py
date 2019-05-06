import numpy as np
import pandas as pd


def json2csv(tables):
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
        #df.to_csv('my_csv.csv', index=False, header=False)





