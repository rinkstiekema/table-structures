import os
import sys
import pandas as pd 
import csv
import numpy as np
import tabula
from tqdm import tqdm 
import io 
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Missing argument. Usage: <pdf location> <gt location>")
        exit(-1)

    pdf_path = sys.argv[1]
    gt_path = sys.argv[2]
    cc = SmoothingFunction()
    for pdf in os.listdir(pdf_path)[2000:]:
        df_pred = tabula.read_pdf(os.path.join(pdf_path, pdf))
        df_gt = pd.read_csv(os.path.join(gt_path, os.path.splitext(pdf)[0]+'.csv'))

        np_pred_row = np.array([df_pred.columns.values.tolist()] + df_pred.values.tolist())
        np_gt_row = np.array([df_gt.columns.values.tolist()] + df_gt.values.tolist())

        np_pred_col = np.transpose(np_pred_row).flatten()
        np_gt_col = np.transpose(np_gt_row).flatten()
        np_pred_row = np_pred_row.flatten()
        np_gt_row = np_gt_row.flatten()
        
        print(df_pred)
        print(df_gt)
        
        print(sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method7), sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method7))

