import os
import random
import sys 

location = sys.argv[1]
images = os.listdir(os.path.join(location, "train_A"))
random.shuffle(images)
original_length = len(images)

types = [{"name":"train", "range": 50}, {"name":"val", "range": 25}, {"name":"test", "range": 25}]
for t in types:
    img_location = os.path.join(location, t["name"])
    if not os.path.exists(img_location):
        os.mkdir(img_location)
    
    label_location = os.path.join(location, t["name"]+"_label")
    if not os.path.exists(label_location):  
        os.mkdir(label_location)

    data = images[:original_length/100 * t["range"])]

    for image in data:
        os.rename(os.path.join(location, "train_A", image), os.path.join(img_location, image))
        os.rename(os.path.join(location, "train_B", image), os.path.join(label_location, image))

    images = images[original_length/100 * t["range"])+1:]