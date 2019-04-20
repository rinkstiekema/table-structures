from sklearn.model_selection import train_test_split
import os
import sys 

location = sys.argv[1]
images = os.listdir(location)
random.shuffle(images)
train_data = images[:int(len(images)/100 * 80)]
test_data = images[int(len(images)/100 * 80):]

try:
    os.mkdir(os.path.join(location, "train"))
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

try:
    os.mkdir(os.path.join(location, "test"))
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

for image in train_data:
    os.rename(location, os.path.join(location, "train"))

for image in test_data:
    os.rename(location, os.path.join(location, "test"))


