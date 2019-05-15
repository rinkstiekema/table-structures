import os
import numpy as np
import json
import cv2
import traceback

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

def get_lines_img(img):
	red = np.array([0,0,255])
	mask = cv2.inRange(img, red, red)
	output_img = img.copy()
	output_img[np.where(mask==0)] = 0
	return output_img

def get_hough_lines(img, verbose=False):
	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	lines = cv2.HoughLinesP(image=img,rho=1,theta=np.pi/180, threshold=10, minLineLength=1, maxLineGap=1)
	lines = list(map(lambda x: [(x[0][0], x[0][1]),(x[0][2], x[0][3])], lines))
	if(verbose):
		for line in lines:
			cv2.line(img, line[0], line[1], (255,255,255),1)
		cv2.imshow("image", img)
		cv2.waitKey(0)

	# Flatten lines list
	return lines

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

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

def rule(json_folder):
	json_file_list = os.listdir(json_folder)

	for json_file in json_file_list:
		json_file_location = os.path.join(json_folder, json_file)
		with open(json_file_location, 'r+') as jfile:
			result = [] # eventually new json file
			tables = json.load(jfile) # current json file
			for table in tables:
				try:
					original_size = (table["regionBoundary"]["x2"] - table["regionBoundary"]["x1"], table["regionBoundary"]["y2"] - table["regionBoundary"]["y1"])
					original_size = (int(original_size[0]*72/25.4), int(original_size[1]*72/25.4))
					img = cv2.imread(table["outlineURL"])[0:int(original_size[1]), 0:int(original_size[0])]
					gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
					img = cv2.Canny(gray, 500, 500,apertureSize = 3)
					kernel = np.ones((3,3),np.uint8)
					img = cv2.dilate(img, kernel,iterations = 1)
					kernel = np.ones((5,5),np.uint8)
					img = cv2.erode(img,kernel,iterations = 1)

					lines = get_hough_lines(img, False)

					intersection_points = []
					for idx, i in enumerate(lines):
						for j in lines[idx+1:]:
							try:
								intersection_points.append(line_intersection(i, j))
							except Exception as e:
								#print(e)
								continue

					intersection_points = list(set(intersection_points))
					intersection_points = fuse(intersection_points, 5)
					intersection_points = align(intersection_points, 10)

					cells = []
					intersection_points.sort()
					for idx, i in enumerate(intersection_points):
						cell = find_cell(i, intersection_points[idx:])
						if cell:
							cells.append(cell)

					test_img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)


					table["cells"] = cells
					result.append(table)
					jfile.seek(0)
					jfile.write(json.dumps(result))
					jfile.truncate()
				except Exception as e:
					print("Skipping step", traceback.format_exc())
					continue
