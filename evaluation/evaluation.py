import os
import sys
import pandas as pd 
import csv
import numpy as np
import tabula
from tqdm import tqdm 
import io 

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Missing argument. Usage: <ground truth location> <prediction location>")
        exit(-1)

    pdf_path = sys.argv[1]
    gt_path = sys.argv[2]

    correct = 0
    wrong = 0
    for pdf in tqdm(os.listdir(pdf_path)[:3000]):
        df_pred = tabula.read_pdf(os.path.join(pdf_path, pdf))
        df_gt = pd.read_csv(os.path.join(gt_path, os.path.splitext(pdf)[0]+'.csv'))
        
        print(df_pred)
        print(df_gt)

        # try:

        #     if df_pred.equals(df_gt):
        #         correct += 1
        #     else: 
        #         wrong += 1
        # except:
        #     wrong += 1
        # print("%i correct | %i wrong"%(correct, wrong))


