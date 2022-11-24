import cv2
import numpy as np

def proc(image):
    blurred_image=cv2.GaussianBlur(image,(5,5),1)
    proc_image=cv2.adaptiveThreshold(blurred_image,255,1,1,11,2)
    return proc_image

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