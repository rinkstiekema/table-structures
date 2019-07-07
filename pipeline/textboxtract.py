from operator import itemgetter 
from itertools import groupby
import os
import json
import fitz
import sys
import time 
import minecart
import utils
from tqdm import tqdm

def texboxtract_synthetic(pdf, table):
    doc = fitz.open(pdf)
    page = doc[int(table["page"])-1]
    words = page.getTextWords()
    for idx, cell in enumerate(table["cells"]):
        rect = [cell[0][0]+table["regionBoundary"]["x1"], cell[0][1]+table["regionBoundary"]["y1"], cell[1][0]+table["regionBoundary"]["x1"], cell[1][1]+table["regionBoundary"]["y1"]]
        rect = list(map(lambda i: i*0.72, rect))

        mywords = [w for w in words if fitz.Rect([(w[0]+w[2])/2,(w[1]+w[3])/2,(w[0]+w[2])/2+1,(w[1]+w[3])/2+1]) in fitz.Rect(rect)]
        mywords.sort(key = itemgetter(3, 0))   # sort by y1, x0 of the word rect
        group = groupby(mywords, key = itemgetter(3))
        
        result = ""
        for y1, gwords in group:
            result += " ".join(w[4] for w in gwords)
        cell = {"cell": cell, "rect": [(rect[0], rect[1]), (rect[2], rect[3])], "words": result}
        table["cells"][idx] = cell
    return table

def texboxtract(pdf, table):
    doc = fitz.open(pdf)
    page = doc[int(table["page"])]
    words = page.getTextWords()
    for idx, cell in enumerate(table["cells"]):
        rect = [cell[0][0]*72/table["renderDpi"]+table["regionBoundary"]["x1"], cell[0][1]*72/table["renderDpi"]+table["regionBoundary"]["y1"], cell[1][0]*72/table["renderDpi"]+table["regionBoundary"]["x1"], cell[1][1]*72/table["renderDpi"]+table["regionBoundary"]["y1"]]

        mywords = [w for w in words if fitz.Rect([(w[0]+w[2])/2,(w[1]+w[3])/2,(w[0]+w[2])/2+1,(w[1]+w[3])/2+1]) in fitz.Rect(rect)]
        mywords.sort(key = itemgetter(3, 0))   # sort by y1, x0 of the word rect
        group = groupby(mywords, key = itemgetter(3))
        
        result = ""
        for y1, gwords in group:
            result += " ".join(w[4] for w in gwords)
        cell = {"cell": cell, "rect": [(rect[0], rect[1]), (rect[2], rect[3])], "words": result}
        table["cells"][idx] = cell
    return table