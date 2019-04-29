import os
import sys
from keras.models import model_from_json
import matplotlib.pyplot as plt
import imageio
#import visvis as vv
import numpy as np

def get_generator():
    json_file = open('./model/generator.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("./model/generator.h5")
    print("Succesfully loaded model")
    return loaded_model

def pad(a):
    """Return bottom right padding."""
    zeros = np.full((1, 1024, 1024, 3), 255)
    zeros[0][0] = 0
    zeros[:, :a.shape[0], :a.shape[1], :a.shape[2]] = a
    return zeros

def get_image(img_path):
    print(img_path)
    img = imageio.imread(img_path, as_gray=False, pilmode="RGB").astype(np.float)
    return pad(img)

def predict(png_folder, results_folder):
    generator = get_generator()
    for png in os.listdir(png_folder):
        img = get_image(os.path.join(png_folder, png))
        generated = generator.predict(img)
        imageio.imwrite(os.path.join(results_folder,png), generated[0].astype('float'))

