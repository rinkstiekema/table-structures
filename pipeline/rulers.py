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

def get_hough_lines(img, verbose=False):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	lines = cv2.HoughLinesP(image=gray,rho=1,theta=np.pi/180, threshold=10, minLineLength=1, maxLineGap=1)
	lines = list(map(lambda x: [(x[0][0], x[0][1]),(x[0][2], x[0][3])], lines))
	if(verbose):
		for line in lines:
			cv2.line(gray, line[0], line[1], (255,255,255),1)
		cv2.imshow("image", gray)
		cv2.waitKey(0)

	# Flatten lines list
	return lines

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = int(det(d, xdiff) / div)
    y = int(det(d, ydiff) / div)
    return x, y

def find_cell(intersection, intersections):
	for i in intersections:
		if intersection[0] < i[0] and intersection[1] < i[1]:
			return (intersection, i)
	return None

def rule(input_folder):
	file_list = os.listdir(input_folder)
	result = {}
	for file_name in file_list:
		print("Ruling: "+file_name)
		img = cv2.imread(os.path.join(input_folder, file_name))
		lines_img = get_lines_img(img)
		lines = get_hough_lines(lines_img, False)[:100]
		intersection_points = []
		print("Finding intersections")
		for idx, i in enumerate(lines):
			for j in lines[idx+1:]:
				try:
					intersection_points.append(line_intersection(i, j))
				except Exception as e:
					#print(e)
					continue
		print("Finding cells in "+str(len(intersection_points))+" points")
		cells = []
		intersection_points.sort()
		for idx, i in enumerate(intersection_points):
			cell = find_cell(i, intersection_points[idx:])
			if cell:
				cells.append(cell)
		result[file_name] = cells
	return result