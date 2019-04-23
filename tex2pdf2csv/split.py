from sklearn.model_selection import train_test_split
import os
import random
import sys 

location = sys.argv[1]
images = os.listdir(location)
random.shuffle(images)
train_data = images[:int(len(images)/100 * 80)]
test_data = images[int(len(images)/100 * 80):]

try:
    os.mkdir(os.path.join(location, "train"))
    print("Directory train Created ") 
except FileExistsError:
    print("Directory train already exists")

try:
    os.mkdir(os.path.join(location, "test"))
    print("Directory test Created ") 
except FileExistsError:
    print("Directory test already exists")

for image in train_data:
    os.rename(location+image, os.path.join(location, "train", image))

for image in test_data:
    os.rename(location+image, os.path.join(location, "test", image))


