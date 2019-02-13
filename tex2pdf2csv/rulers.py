import sys
import os
import cv2
import numpy as np
import pandas as pd
import json

def get_lines_img(img):
	red = np.array([0,0,255])
	mask = cv2.inRange(img, red, red)
	output_img = img.copy()
	output_img[np.where(mask==0)] = 0
	return output_img

def get_hough_lines(img, verbose):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	lines = cv2.HoughLinesP(image=gray,rho=1,theta=np.pi/180, threshold=10, minLineLength=1, maxLineGap=1)
	
	if(verbose):
		for line in lines:
			for x1, y1, x2, y2 in line:
				cv2.line(gray,(x1,y1),(x2,y2),(255,255,255),1)
		cv2.imshow("image", gray)
		cv2.waitKey(0)

	# Flatten lines list
	return list(map(lambda x: x[0].tolist(), lines))

if(len(sys.argv) < 2):
	print("Missing arguments. Usage: <input-folder>")

input_folder = sys.argv[1]
file_list = [x for x in os.listdir(input_folder) if "noborders" not in x and os.path.splitext(x)[1] == ".png"]

result = {}

for file in file_list:
	img = cv2.imread(input_folder + '/' + file)
	lines_img = get_lines_img(img)
	result[file] = get_hough_lines(lines_img, True)

print(result)
with open('json/rulers.json', 'w') as outfile:
	json.dump(result, outfile)
	# cv2.imshow("image", lines_img)
	# cv2.waitKey(0)

