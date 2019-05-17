import os
import random
import sys 

location = sys.argv[1]
images = os.listdir(os.path.join(location, "train_A"))
random.shuffle(images)
original_length = len(images)

types = [{"name":"train", "range": 50}, {"name":"val", "range": 25}, {"name":"test", "range": 25}]
for t in types:
    try:
        os.mkdir(os.path.join(location, t["name"]))
    try:
        os.mkdir(os.path.join(location, t["name"]+"_label"))

    data = images[:original_length/100 * t["range"])]

    for image in data:
        os.rename(os.path.join(location, "train_A", image), os.path.join(location, t["name"], image))
        os.rename(os.path.join(location, "train_B", image), os.path.join(location, t["name"]+"_label", image))

    images = images[original_length/100 * t["range"])+1:]