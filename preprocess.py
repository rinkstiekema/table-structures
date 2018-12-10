import os
import cv2
import pandas as pd

root_dir = os.getcwd()
file_list = ['train.csv', 'val.csv']
data_root = os.path.join(os.path.dirname(root_dir), 'data')
image_source_dir = data_root + '\images'
for file in file_list:
    image_target_dir = os.path.join(data_root, file.split(".")[0])
    
    # read list of image files to process from file
    image_list = pd.read_csv(os.path.join(data_root, file), header=None)[0]
    
    print("Start preprocessing images")
    for image in image_list:
        # open image file
        img = cv2.imread(os.path.join(image_source_dir, image))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # perform transformations on image
        b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
        g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
        r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)
        
        # merge the transformed channels back to an image
        transformed_image = cv2.merge((b, g, r))
        target_file = os.path.join(image_target_dir, image)

        print("Writing target file {}".format(target_file))
        print(cv2.imwrite(target_file, transformed_image))