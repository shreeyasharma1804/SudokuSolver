import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from utils import functions, backtrack
import sys

solved_sudoku = []


def main():

    model=functions.initializePredictionModel()
    path = os.getcwd()
    Im=cv2.imread(os.path.join(path ,'utils','suduko.png'),0)
    widthImg=360
    heightImg=360
    Image=cv2.resize(Im,(widthImg,heightImg))

    blank_image=np.zeros((heightImg,widthImg,3),np.uint8)
    corrected_image=functions.proc(Image)
    imgContour=Image.copy()
    imgBigContour=Image.copy()

    contours, hierarchy=cv2.findContours(corrected_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContour,contours, -1,(0,255,0),3)

    biggest,maxArea=functions.biggestContour(contours)

    if biggest.size !=0:

        biggest_reorder =functions.reorder(biggest)
        cv2.drawContours(imgBigContour,biggest_reorder,-1,(0,255,0),10)
        points1=np.float32(biggest_reorder)
        points2=np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
        matrix=cv2.getPerspectiveTransform(points1, points2)
        imageWarpColor=cv2.warpPerspective(Image,matrix,(widthImg,heightImg))
        boxes, zeros =functions.splitBoxes(255-imageWarpColor)
        obtained_sudoku = np.array(functions.getPredection(boxes, zeros, model))
        obtained_sudoku = np.reshape(obtained_sudoku,(9,9))
        obtained_sudoku_cpy = obtained_sudoku.copy()
        global solved_sudoku
        solved_sudoku = backtrack.solveSudoku(obtained_sudoku_cpy)

        for i in range(9):
            for j in range(9):
                if(obtained_sudoku[i][j] == 0):
                    imageWarpColor = cv2.putText(imageWarpColor, str(solved_sudoku[i][j]), (40*j+20, 40*i+30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 0), 2, cv2.LINE_AA)
        
        cv2.imwrite("solved.png", imageWarpColor)


def return_sudoku():
    return solved_sudoku
