import sys
import os
import argparse
import random 
from pprint import pprint

def pick_multicolumn_indices(array):
    amount = random.randint(1, len(array)-4)
    return sorted(random.sample(range(2, len(array)-2), amount))

def create_multicolumn(array1, array2, indices):
    # Loop over each line that needs to be multicolumned
    for i in indices:       
        # Split the line into cells
        splitted1 = r"\\".join(array1[i].split(r"\\")[0:-1]).split("&")
        ending1 = array1[i].split(r"\\")[-1]
        splitted2 = r"\\".join(array2[i].split(r"\\")[0:-1]).split("&")
        ending2 = array2[i].split(r"\\")[-1]
        result = []
        
        # Loop over the cells in the column
        j = 0
        while j < len(splitted):
            # The amount of cells that will be combined in this loop
            to_combine = random.randint(1, len(splitted)-j)

            # The string that will replace the cell nad  all the cells that are combined into it
            multicolumn_string = '\multicolumn{%s}{c}{%s}'%(to_combine, splitted[j])
            result.append(multicolumn_string)
            j += to_combine
        array[i] = "&".join(result) + r"\\" + ending

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, help='Path to save the dataset')
    parser.add_argument('--amount', type=int, default=1, help='How many tables should be transformed')
    args = parser.parse_args()

    root = args.folder
    tex_folder = os.path.join(root, 'tex', 'val')
    tex_skeleton_folder = os.path.join(root, 'tex', 'val_labels')

    items = list(map(lambda x: os.path.join(tex_folder, x),os.listdir(tex_folder)[0:args.amount]))
    items_skeleton = list(map(lambda x: os.path.join(tex_skeleton_folder, x), os.listdir(tex_skeleton_folder)[0:args.amount]))
    for idx, item in enumerate(items):
        with open(item, 'r+') as tex, open(items_skeleton[idx], 'r+') as tex_skeleton:
            content = [x.strip() for x in tex.readlines() if x.strip() is not '']
            content_skeleton = [x.strip() for x in tex_skeleton.readlines() if x.strip() is not '']

            multicolumn_indices = pick_multicolumn_indices(content)
            content, content_skeleton = create_multicolumn(content, content_skeleton, multicolumn_indices)
            
