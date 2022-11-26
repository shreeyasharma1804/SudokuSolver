import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model
import os
#hello world
path = os.getcwd()
constant=255
def initializePredictionModel():
    model=load_model(os.path.join(path ,'utils','digit_recognition.h5'))
    
    return model
def proc(image):
    blurred_image=cv2.GaussianBlur(image,(5,5),1)
    proc_image=cv2.adaptiveThreshold(blurred_image,constant,1,1,11,2)
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


def splitBoxes(image):
    rows=np.vsplit(image,9)
    boxes=[]
    for row in rows:
        cols=np.hsplit(row,9)
        for box in cols:
            boxes.append(box)
    return boxes


def getPredection(boxes,model):
    result=[]
    for image in boxes:
        # image=np.asarray(image)
        # image=image[4:image.shape[0]-4,4:image.shape[1]-4]
        image=cv2.resize(image,(28,28))
        # image=image/255
        image=image.reshape(1,28,28,1)
        image = image.astype("float32")/255
        predictions=model.predict(image)
        classIndex=np.argmax(predictions)
        probability_value=np.amax(predictions)

        if probability_value> 0.8:
            result.append(classIndex)
        else:
            result.append(0)

    print("Debug: ", result)
    return result
             