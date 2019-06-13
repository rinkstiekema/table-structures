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
    for path in os.listdir(pred_path):
        df_pred = pd.read_csv(os.path.join(pred_path, os.path.splitext(path)[0]+'.csv'))
        df_gt = pd.read_csv(os.path.join(gt_path, os.path.splitext(path)[0]+'.csv'))

        np_pred_row = np.array([df_pred.columns.values.tolist()] + df_pred.values.tolist())
        np_gt_row = np.array([df_gt.columns.values.tolist()] + df_gt.values.tolist())

        np_pred_col = np.transpose(np_pred_row).flatten()
        np_gt_col = np.transpose(np_gt_row).flatten()
        np_pred_row = np_pred_row.flatten()
        np_gt_row = np_gt_row.flatten()
        
        result_list.append([path,
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method0),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method0),
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method1),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method1),
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method2),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method2),
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method3),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method3),
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method4),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method4),
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method5),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method5),
        # sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method6),
        # sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method6),
        sentence_bleu([np_gt_col], np_pred_col, smoothing_function=cc.method7),
        sentence_bleu([np_gt_row], np_pred_row, smoothing_function=cc.method7)])
    result_df = pd.DataFrame(result_list, columns=['file', 'bleu_col7', 'bleu_row7'])
    result_df.to_csv(scores_path)
        
