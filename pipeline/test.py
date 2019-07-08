import sys
import os
import cv2 
import rulers 

png = cv2.imread(sys.argv[1])
cells, intersections = rulers.rule_test(png)
print(intersections)
for cell in cells:
    cv2.rectangle(png, cell[0], cell[1], (0,0,0),1)

# for intersection in intersections:
#     cv2.circle(png, intersection, 1, (0,0,0),1)

cv2.imshow('image', png)
cv2.waitKey(0)
cv2.destroyAllWindows()