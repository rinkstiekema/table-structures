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
    if(len(sys.argv) < 4):
        print("Missing argument. Usage: <pred location> <ground truth location> <scores location>")
        exit(-1)

    pred_path = sys.argv[1]
    gt_path = sys.argv[2]
    scores_path = sys.argv[3]
    cc = SmoothingFunction()
    result_list = []
    for path in tqdm(os.listdir(pred_path)):
        try:
            df_pred = pd.read_csv(os.path.join(pred_path, os.path.splitext(path)[0]+'.csv'), dtype=str)
            df_gt = pd.read_csv(os.path.join(gt_path, os.path.splitext(path)[0]+'.csv'), index_col=[0], dtype=str)
            df_pred.columns = df_pred.loc[0]

            # drop completely empty rows and columns
            df_pred = df_pred.dropna(how='all', axis=0)
            df_pred = df_pred.dropna(how='all', axis=1)
            
            # make the first row the header
            new_header = df_pred.iloc[0]
            df_pred = df_pred[1:]
            df_pred.columns = new_header

            np_pred_row = np.array([df_pred.columns.values.tolist()] + df_pred.values.tolist())
            np_gt_row = np.array([df_gt.columns.values.tolist()] + df_gt.values.tolist())

            np_pred_col = " ".join(np.transpose(np_pred_row).flatten())
            np_gt_col = " ".join(np.transpose(np_gt_row).flatten())
            np_pred_row = " ".join(np_pred_row.flatten())
            np_gt_row = " ".join(np_gt_row.flatten())

            result_list.append([path,
            sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method6),
            sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method6)])
        except:
            result_list.append([path, 0, 0])
            continue

    result_df = pd.DataFrame(result_list, columns=['file', 'bleu_col7', 'bleu_row7'])

    grouped = result_df.copy()
    grouped['category'] = grouped['file'].apply(lambda x: x.split("-")[0])
    grouped['file'] = grouped['file'].apply(lambda x: x.split("-")[1])
    
    result_df.to_csv(scores_path)
    grouped.groupby('category').mean().to_csv(os.path.splitext(scores_path)[0] + '-grouped' + '.csv')        
