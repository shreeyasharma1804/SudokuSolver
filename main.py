
if __name__ == "__main__":
    import cv2
    import numpy as np
    import os
    import matplotlib.pyplot as plt
    from utils import proc,biggestContour
#%% Reading the image file
    path = os.getcwd()
    Im=cv2.imread(os.path.join(path ,'utils','suduko_image.jpg'),0)
    Image=cv2.resize(Im,(256,256))
#%%Correcting the image and contouring
    corrected_image=proc.proc(Image)
    imgContour=Image.copy()
    imgBigContour=Image.copy()
    contours, hierarchy=cv2.findContours(corrected_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContour,contours, -1,(0,255,0),3)
    biggest,maxArea=biggestContour.biggestContour(contours)
    plt.imshow(biggest)
    plt.show()
    