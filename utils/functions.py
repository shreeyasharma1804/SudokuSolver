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

def reorder(mypoints):
    mypoints=mypoints.reshape((4,2))
    mypointsNew=np.zeros((4,1,2),dtype=np.int32)
    sum=mypoints.sum(1)
    mypointsNew[0]=mypoints[np.argmin(sum)]
    mypointsNew[3]=mypoints[np.argmax(sum)]
    sub=np.diff(mypoints,axis=1)
    mypointsNew[1]=mypoints[np.argmin(sub)]
    mypointsNew[2]=mypoints[np.argmax(sub)]
    return mypointsNew
    
