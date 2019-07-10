import os
import numpy as np
import json
import cv2
import imageio
import traceback
import random
import utils
from multiprocessing import Pool
from functools import partial
from tqdm import tqdm

def line_intersection_strict(line1, line2):
	if line1[0][0] == line1[1][0]:
		return line1[0][0] > line2[0][0] and line1[0][0] < line2[1][0] and line1[0][1] < line2[0][1] and line1[1][1] > line2[1][1]
	else:
		return line1[0][0] < line2[0][0] and line1[1][0] > line2[1][0] and line2[0][1] < line1[0][1] and line2[1][1] > line1[1][1] 

def unique_intersections(intersections):
	return list(set(intersections))

def get_hough_lines(img):
	lines = cv2.HoughLinesP(image=img,rho=1,theta=np.pi/180, threshold=40, minLineLength=5, maxLineGap=1)
	lines = list(map(lambda x: [(x[0][0], x[0][1]), (x[0][2], x[0][3])], lines))
	return lines

def line_intersection(line1, line2, regionBoundary):
	s = np.vstack([line1[0], line1[1], line2[0], line2[1]])        # s for stacked
	h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
	l1 = np.cross(h[0], h[1])           # get first line
	l2 = np.cross(h[2], h[3])           # get second line
	x, y, z = np.cross(l1, l2)          # point of intersection
	if z == 0:                          # lines are parallel
		return False

	x = x/z
	y = y/z
	
	max_x = (regionBoundary["x2"] - regionBoundary["x1"])/72*150 + 20
	max_y = (regionBoundary["y2"] - regionBoundary["y1"])/72*150 + 20

	# Check if intersection is within regionBoundary
	if(x < -20 or x > max_x or y < -20 or y > max_y):
		return False
	return int(x), int(y)

def preprocess_image(img):
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_CONSTANT,value=(255,255,255))
	low_threshold = 50
	high_threshold = 150
	img = cv2.Canny(img, low_threshold, high_threshold)
	kernel = np.ones((3,3),np.uint8)
	img = cv2.dilate(img, kernel, iterations = 1)
	kernel = np.ones((5,5),np.uint8)
	img = cv2.erode(img,kernel, iterations = 1, borderType=cv2.BORDER_CONSTANT)
	img = img[10:len(img[0])-10, 10:len(img[1])-10]
	return img

def get_intersections(lines, regionBoundary):
	intersection_points = []
	for idx, i in enumerate(lines):
		for j in lines[idx+1:]:
			intersection = line_intersection(i, j, regionBoundary)
			if not intersection:
				continue
			intersection_points.append(intersection)
	return intersection_points

def get_cells(intersection_points):
	cells = []

	x_points = list(map(lambda item: item[0], intersection_points))
	y_points = list(map(lambda item: item[1], intersection_points))
	# x_points = list(set(sorted(filter(lambda x: x_points.count(x) > 3, x_points))))
	# y_points = list(set(sorted(filter(lambda y: y_points.count(y) > 3, y_points))))
	x_points = sorted(list(set(x_points)))
	y_points = sorted(list(set(y_points)))
	
	for idx_y, y in enumerate(y_points[:-1]):
		for idx_x, x in enumerate(x_points[:-1]):
			cells.append([(x,y), (x_points[idx_x+1],y_points[idx_y+1])])
	cells = list(filter(lambda cell: cell[1][0] - cell[0][0] > 10 and cell[1][1] - cell[0][1] > 10, cells))

	return cells

def rule(table, pdf, opt):
	img = cv2.imread(os.path.splitext(table["renderURL"])[0].replace("png", "outlines_"+opt.model)+".png")	
	img = preprocess_image(img)

	lines = get_hough_lines(img)
	page = pdf[int(table["page"])]
	words = page.getTextWords()

	intersection_points = get_intersections(lines, table["regionBoundary"])
	intersection_points = unique_intersections(intersection_points)

	cells = get_cells(intersection_points)

	table["cells"] = cells
	table["name"] = os.path.splitext(os.path.basename(table["renderURL"]))[0]
	return table

def rule_test(img):
	img = preprocess_image(img)

	lines = get_hough_lines(img)

	intersection_points = get_intersections(lines, {"x1":0, "x2":1024, "y1":0, "y2": 1024})
	intersection_points = unique_intersections(intersection_points)

	cells = get_cells(intersection_points)
	return cells, intersection_points