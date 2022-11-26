
if __name__ == "__main__":
    import cv2
    import numpy as np
    import os
    import matplotlib.pyplot as plt
    from utils import functions
    model=functions.initializePredictionModel()
#%% Reading the image file
    path = os.getcwd()
    Im=cv2.imread(os.path.join(path ,'utils','suduko_image.jpg'),0)
    widthImg=360
    heightImg=360
    constant=255
    Image=cv2.resize(Im,(widthImg,heightImg))
    blank_image=np.zeros((heightImg,widthImg,3),np.uint8)
#%%Correcting the image and contouring
    corrected_image=functions.proc(Image)
    imgContour=Image.copy()
    imgBigContour=Image.copy()

    contours, hierarchy=cv2.findContours(corrected_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContour,contours, -1,(0,constant,0),3)
    biggest,maxArea=functions.biggestContour(contours)
    if biggest.size !=0:
        biggest_reorder =functions.reorder(biggest)
        cv2.drawContours(imgBigContour,biggest_reorder,-1,(0,constant,0),10)
        points1=np.float32(biggest_reorder)
        points2=np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
        matrix=cv2.getPerspectiveTransform(points1, points2)
        #%%Splitting the digits
        imageWarpColor=cv2.warpPerspective(Image,matrix,(widthImg,heightImg))
        imageDetectedDigits=blank_image.copy()
        # imageWarpColor=cv2.cvtColor(imageWarpColor,cv2.COLOR_BGR2GRAY)
        imageSolvedDigits=blank_image.copy()
        print(imageWarpColor.shape)
        boxes=functions.splitBoxes(imageWarpColor)
        
        print(len(boxes))
        #calling the model 
        numbers=functions.getPredection(boxes,model)
        print(numbers)
        # imageDetectedDigits=functions.displayNumbers(imageDetectedDigits,numbers,color=(255,0,255))
        # numbers=np.asarray(numbers)
        # positive_array=np.where(numbers>0,0,1)