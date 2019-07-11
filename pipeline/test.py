import sys
import os
import cv2 
import rulers 
import pad

directory = sys.argv[1]
for i in os.listdir(directory):
    pad.pad_image(os.path.join(directory, i), (1024, 1024))

# png = cv2.imread(sys.argv[1])
# cells, intersections, img = rulers.rule_test(png)
# print(intersections)
# # for cell in cells:
# #     cv2.rectangle(png, cell[0], cell[1], (),1)
# img = cv2.cvtColor(img,cv2.COLOR_GRAY2B)
# for intersection in intersections:
#     cv2.circle(img, intersection, 1, (255,0,0), 3)

# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
