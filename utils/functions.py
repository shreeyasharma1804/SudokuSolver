import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model
import os
import matplotlib.pyplot as plt

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

def dfs(image, i, j, new_box):
    if(i >= image.shape[0] or j >= image.shape[1] or new_box[i][j] == 255):
        return
    if(image[i][j] == 255):
        new_box[i][j] = 255
        dfs(image, i+1, j, new_box)
        dfs(image, i-1, j, new_box)
        dfs(image, i, j+1, new_box)
        dfs(image, i, j-1, new_box)
    else:
        return

def splitBoxes(image):
    kernel = np.ones((3, 3), np.uint8)
    rows=np.vsplit(image,9)
    boxes=[]
    zeros = {}
    i = 0
    for row in rows:
        cols=np.hsplit(row,9)
        for box in cols:
            box = cv2.dilate(box, kernel, iterations=1)
            new_box = [[0 for i in range(40)] for j in range(40)]
            ret,box = cv2.threshold(box,127,255,cv2.THRESH_BINARY)
            x = box.shape[0]//2
            is_Zero = True
            for y in range(box.shape[1]//2-10, box.shape[1]//2+10):
                if(box[x][y] == 255):
                    is_Zero = False
                    dfs(box, x, y, new_box)
                    break
            if(is_Zero):
                zeros[i] = 1
            boxes.append(np.array(new_box))
            i+=1
    return boxes, zeros

def undesired_objects (image):
    image = image.astype('uint8')
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    sizes = stats[:, -1]

    max_label = 1
    max_size = sizes[1]
    for i in range(2, nb_components):
        if sizes[i] > max_size:
            max_label = i
            max_size = sizes[i]

    img2 = np.zeros(output.shape)
    img2[output == max_label] = 255
    return img2


def getPredection(boxes, zeros, model):
    result=[]
    i = 0
    for image in boxes:
        if(i in zeros):
            result.append(0)
        else:
            image=cv2.resize(image.astype("float32"),(28,28))
            image=image.reshape(1,28,28,1)
            image = image.astype("float32")/255
            predictions=model.predict(image, verbose=0)
            classIndex=np.argmax(predictions)
            probability_value=np.amax(predictions)
            result.append(classIndex)
        i+=1
    return result
             