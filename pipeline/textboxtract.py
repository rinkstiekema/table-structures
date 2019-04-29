from operator import itemgetter 
from itertools import groupby
import fitz
import sys

def texboxtract(pdf, tables):
    for table in tables:
        doc = fitz.open(pdf)
        page = doc[int(table["page"])]
        words = page.getTextWords()
        for cell in table["cells"]:
            rect = [cell[0][0], cell[0][1], cell[1][0], cell[1][1]]
            
            mywords = [w for w in words if fitz.Rect(w[:4])in fitz.Rect(rect)]
            mywords.sort(key = itemgetter(3, 0))   # sort by y1, x0 of the word rect
            group = groupby(mywords, key = itemgetter(3))
            
            result = ""
            for y1, gwords in group:
                result += " ".join(w[4] for w in gwords)
            cell.append(result)
    return tables