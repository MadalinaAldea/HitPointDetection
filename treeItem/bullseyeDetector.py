import cv2
import numpy as np 

def createBullseyeDetector(src):
    morph = __morphImage(src.copy())
    hull = __convexHull(morph)
    bullseye = cv2.fitEllipse(hull)
    
    return bullseye

def __morphImage(src):
    kernel = np.ones((2, 2), np.uint8)
    grayImg = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[-1]
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    return opening

def __convexHull(src):
        contour_list = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        bullseye = max(contour_list, key = cv2.contourArea)
        hull = cv2.convexHull(bullseye)

        return hull