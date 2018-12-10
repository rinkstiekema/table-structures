import os
import cv2
import imutils
import copy
import numpy as np

def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
 
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
 
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
 
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))
 
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

if __name__ == "__main__":
    in_file = os.path.join("in", "in7.jpg")
    out_file = os.path.join("out", "out-final.png")

    img = cv2.imread(os.path.join(in_file))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    (thresh, img_bin) = cv2.threshold(gray, 128, 255,cv2.THRESH_BINARY, cv2.THRESH_OTSU)
    img_bin = 255-img_bin 
    cv2.imwrite("out/img_bin.jpg",img_bin)


    kernel_length = np.array(img).shape[2]
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))    
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=10)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=10)
    cv2.imwrite("out/verticle_lines.jpg",verticle_lines_img)

    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=10)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=10)
    cv2.imwrite("out/horizontal_lines.jpg",horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite("out/img_final_bin.jpg",img_final_bin)

    # Find contours for image, which will detect all the boxes
    im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")


    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)
        if (h > 100 and h < img.shape[0]):
            idx += 1
            new_img = img[y:y+h, x:x+w]
            cv2.imwrite("out/out"+str(idx) + '.png', new_img)
            # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
            if (w > 80 and h > 20) and w > 3*h:
                idx += 1
                new_img = img[y:y+h, x:x+w]
                cv2.imwrite("out/out"+str(idx) + '.png', new_img)