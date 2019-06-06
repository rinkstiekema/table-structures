import sys
import os
import textract
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

if len(sys.argv) < 3:
    print("Missing arguments. Usage: <pdf-location> <csv-location>")    
    exit(-1)

pdf_path = sys.argv[1]
csv_path = sys.argv[2]

text = textract.process(pdf_path).decode("utf-8") 
csv = textract.process(csv_path).decode("utf-8")

text = preprocess(text)
csv = preprocess(csv)
print(csv)
pprint(set([i for i in text if i in csv and i[1] == 'NNP']))
# print(list(filter(lambda x: x[0] == 'AP', csv_iob_tagged)))

# sent1 = preprocess(csv)
# cp1 = nltk.RegexpParser(pattern)
# cs1 = cp.parse(sent1)
# iob_tagged1 = tree2conlltags(cs1)
# pprint(iob_tagged1)
# pprint([i for i in iob_tagged if i[0] == 'AP'])
# pprint(set([i for i in iob_tagged if i in iob_tagged1 and i[1] == 'NNP']))
