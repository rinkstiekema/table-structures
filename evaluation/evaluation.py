import os
import sys
import pandas as pd 

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Missing argument. Usage: <ground truth location> <prediction location>")
        exit(-1)

    gt_location = sys.argv[1]
    pred_location = sys.argv[2]
    for f in os.listdir(gt_location):
        gt_csv = pd.read_csv(os.path.join(gt_location, f))
        pred_csv = pd.read_csv(os.path.join(pred_location), f))
        