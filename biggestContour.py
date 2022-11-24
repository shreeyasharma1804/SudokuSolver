import numpy as np
import cv2
def biggestContour(contours):
    biggest=np.array([])
    maxArea=0
    for i in contours:
        area=cv2.contourArea(i)
        if(area>50):
            perimeter=cv2.arcLength(i,True)
            sides_approx=cv2.approxPolyDP(i,0.02*perimeter,True)
            if(area>maxArea and len(sides_approx)==4):
                biggest=sides_approx
                maxArea=area
    return biggest,maxArea