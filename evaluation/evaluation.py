import os
import sys
import pandas as pd 
import csv
import numpy as np

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Missing argument. Usage: <ground truth location> <prediction location>")
        exit(-1)

    gt_location = sys.argv[1]
    pred_location = sys.argv[2]
    for f in os.listdir(gt_location):
        with open(os.path.join(gt_location, f)) as gt_file, open(os.path.join(pred_location, f)) as pred_file:
            gt = csv.reader(gt_file)
            pred = csv.reader(pred_file)
            gt = list(map(list, zip(*[x for x in gt])))
            pred = list(map(list, zip(*[x for x in pred])))
            
            

