import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os
import json
import cv2
from collections import Counter
from skimage import data
from skimage.feature import match_template
import pandas as pd

fontHeight = 16

def getImages(file):
    with open(file) as jsonFile:
        file_list = json.loads(jsonFile.read())
        result = []
        for i in file_list:
            result.append({'image': i['renderURL'], 'words': i['imageText']})
        return result

def createTextImage(text):
    fnt = ImageFont.truetype("../data/font/cmu.serif-roman.ttf", fontHeight)
    size = fnt.getsize(text)

    # Create a black image
    img = Image.new('RGB', size, color = 'white')
    d = ImageDraw.Draw(img)
    d.text((0,0), text, font=fnt, fill='black')
    
    img.save("../data/word.png")

def matchTemplate(image, word, count, verbose=False):
    matched_template = match_template(image, word)
    max_values = np.argpartition(matched_template, -count, axis=None)[-count:]
    result = []

    for max_value in max_values:
        ij = np.unravel_index(max_value, matched_template.shape)
        x, y = ij[::-1]
        height, width = word.shape

        if(verbose):
            fig = plt.figure(figsize=(8, 3))
            ax1 = plt.subplot(1, 3, 1)
            ax2 = plt.subplot(1, 3, 2)
            ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

            ax1.imshow(word, cmap=plt.cm.gray)
            ax1.set_axis_off()
            ax1.set_title('template')

            ax2.imshow(image, cmap=plt.cm.gray)
            ax2.set_axis_off()
            ax2.set_title('image')
            # highlight matched region
            hcoin, wcoin = word.shape
            rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
            ax2.add_patch(rect)

            ax3.imshow(matched_template)
            ax3.set_axis_off()
            ax3.set_title('`match_template`\nresult')
            # highlight matched region
            ax3.autoscale(False)
            ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

            plt.show()
        result.append({'x1': x, 'x2': x+width, 'y1': y+height, 'y2': y})
    return result;

def create_df(bb_dict):
    result = {}
    for word, bounding_boxes in bb_dict.items():
        for bounding_box in bounding_boxes:
            if(bounding_box['y2'] in result):
                result[bounding_box['y2']].append(word)
            else:
                result[bounding_box['y2']] = [word]
    return pd.DataFrame.from_dict(result, orient='index').sort_index()

def create_cells(bb_dict):
    cells = []
    for word, bounding_boxes in bb_dict.items():
        for bounding_box in bounding_boxes:   
            added = False      
            for cell in cells:
                if (abs(cell['bounding_box']['y1'] - bounding_box['y2']) < fontHeight or abs(cell['bounding_box']['y2'] - bounding_box['y1']) < fontHeight ) and (abs(cell['bounding_box']['x2'] - bounding_box['x1']) < fontHeight or abs(cell['bounding_box']['x1'] - bounding_box['x2']) < fontHeight):
                    cell['content'].append(word)
                    cell['bounding_box'] = { 'x1': min(bounding_box['x1'], cell['bounding_box']['x1']), 'x2': max(bounding_box['x2'], cell['bounding_box']['x2']), 
                                             'y1': max(bounding_box['y1'], cell['bounding_box']['y1']), 'y2': min(bounding_box['y2'], cell['bounding_box']['y2'])}
                    added = True                                             
                    break
            if not added:
                cells.append({'bounding_box': bounding_box, 'content': [word]})
    for cell in cells:
        print(cell['content'])



images = getImages("../data/output-json/Recognition of tables and forms.json")

for image_context in images[1:]:
    image_url = "../data/table-images/"+image_context['image'].split("\\")[-1]
    image = cv2.imread(image_url, cv2.IMREAD_GRAYSCALE) 
    result = {}
    counted_words = dict((x, image_context['words'].count(x)) for x in set(image_context['words']))
    for word, count in counted_words.items():
        createTextImage(word)
        word_image = cv2.imread("../data/word.png", cv2.IMREAD_GRAYSCALE)
        result[word] = matchTemplate(image, word_image, count)
    #df = create_df(result)
    cells = create_cells(result)
    exit()