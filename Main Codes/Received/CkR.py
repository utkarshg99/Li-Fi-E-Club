import cv2 as cv
import numpy as np
img=cv.imread('Circle.png',0)
a,bimg=cv.threshold(img,150,255,cv.THRESH_BINARY_INV)
circles=cv.HoughCircles(bimg,cv.HOUGH_GRADIENT,1,200,250,50,10,0)
print circles
   