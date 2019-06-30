import os
import numpy as np
import json
import cv2
import imageio
import traceback
import random
from multiprocessing import Pool
from functools import partial
from tqdm import tqdm

def align(points, d):
    n = len(points)
    for i in range(n):
        for j in range(n):
            if abs(points[i][0] - points[j][0]) < d:
                mean = (points[i][0] + points[j][0]) / 2
                points[i] = (int(mean), points[i][1])
                points[j] = (int(mean), points[j][1])
            if abs(points[i][1] - points[j][1]) < d:
                mean = (points[i][1] + points[j][1]) / 2
                points[i] = (points[i][0], int(mean))
                points[j] = (points[j][0], int(mean))
    return points

def dist2(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def fuse(points, d):
    ret = []
    d2 = d * d
    n = len(points)
    taken = [False] * n
    for i in range(n):
        if not taken[i]:
            count = 1
            point = [points[i][0], points[i][1]]
            taken[i] = True
            for j in range(i+1, n):
                if dist2(points[i], points[j]) < d2:
                    point[0] += points[j][0]
                    point[1] += points[j][1]
                    count+=1
                    taken[j] = True
            point[0] /= count
            point[1] /= count
            ret.append((int(point[0]), int(point[1])))
    return ret

def unique_intersections(intersections):
	return list(set(intersections))

def get_lines_img(img):
	red = np.array([0,0,255])
	mask = cv2.inRange(img, red, red)
	output_img = img.copy()
	output_img[np.where(mask==0)] = 0
	return output_img

def get_hough_lines(img):
	lines = cv2.HoughLinesP(image=img,rho=1,theta=np.pi/180, threshold=5, minLineLength=1, maxLineGap=1)
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

def find_cell(intersection, intersections):
	for i in intersections:
		if intersection[0] < i[0] and intersection[1] < i[1]:
			width = i[0] - intersection[0]
			height = i[1] - intersection[1]
			if width < 20 or height < 10:
				return None
			else:
				return (intersection, i)
	return None

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
	return img[10:len(img[0])-10, 10:len(img[1])-10]

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

def rule_json_file(json_file, json_folder, opt):
	json_file_location = os.path.join(json_folder, json_file)
	with open(json_file_location, 'r+') as jfile:
		result = [] # eventually new json file
		tables = json.load(jfile) # current json file
		for table in tables:
			try:
				img = cv2.imread(os.path.splitext(table["renderURL"])[0].replace("png", "outlines_"+opt.model)+".png")	
				img = preprocess_image(img)

				lines = get_hough_lines(img)

				intersection_points = get_intersections(lines, table["regionBoundary"])
				intersection_points = unique_intersections(intersection_points)

				cells = get_cells(intersection_points)

				table["cells"] = cells
				table["name"] = os.path.splitext(os.path.basename(table["renderURL"]))[0]
				result.append(table)
				jfile.seek(0)
				jfile.write(json.dumps(result))
				jfile.truncate()
			except Exception as e:
				print("Error when ruling for %s | error: %s" % (json_file, e))
				continue

def rule_pdffigures(json_folder, outlines_folder, opt):
	json_file_list = os.listdir(json_folder)

	pool = Pool()                         
	pool.map(partial(rule_json_file, json_folder=json_folder, opt=opt), json_file_list)


def rule(json_folder, outlines_folder, opt):
	json_file_list = os.listdir(json_folder)

	pool = Pool()                         
	pool.map(partial(rule_json_file, json_folder=json_folder, opt=opt), json_file_list)
	
	json_file_list = os.listdir(json_folder)

	# for json_file in json_file_list:
	# 	json_file_location = os.path.join(json_folder, json_file)
	# 	with open(json_file_location, 'r+') as jfile:
	# 		result = [] # eventually new json file
	# 		tables = json.load(jfile) # current json file
	# 		for table in tables:
	# 			try:
	# 				img = cv2.imread(os.path.join(outlines_folder, table["name"]+'.png'))
	# 				img = preprocess_image(img)

	# 				lines = get_hough_lines(img)

	# 				intersection_points = get_intersections(lines, table["regionBoundary"])
	# 				intersection_points = unique_intersections(intersection_points)

	# 				cells = get_cells(intersection_points)

	# 				table["cells"] = cells
	# 				table["name"] = os.path.splitext(os.path.basename(table["renderURL"]))[0]
	# 				result.append(table)
	# 				jfile.seek(0)
	# 				jfile.write(json.dumps(result))
	# 				jfile.truncate()
	# 			except Exception as e:
	# 				print("Skipping step", traceback.format_exc())
	# 				continue