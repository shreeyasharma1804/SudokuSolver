import cv2
import numpy as np

def proc(image):
    blurred_image=cv2.GaussianBlur(image,(5,5),1)
    proc_image=cv2.adaptiveThreshold(blurred_image,255,1,1,11,2)
    return proc_image
