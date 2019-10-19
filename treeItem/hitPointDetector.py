import cv2
import numpy as np
from PyQt5.QtCore import QPoint

from treeItem.data.svm import predict

def createHitPointDetector(src, scoreRings):
    cv2.cvtColor(src, cv2.COLOR_RGB2BGR, src)

    median = cv2.medianBlur(src, 5)
    gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)

    POIs = __houghCircleTransform(gray)
    POIs = np.asarray(__coordinateList(POIs))

    probabilities = np.asarray( predict(src, POIs)[:,1] )

    hitPoints = __filter(POIs, probabilities, 0.7)
    hitPoints = __scores(scoreRings, hitPoints)
    
    return hitPoints

def __houghCircleTransform(src):
    hough_points = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, dp=1, minDist=40, param1=200, param2=10, minRadius=5, maxRadius=30)[0]
    hough_points = np.uint16(np.around(hough_points))

    return hough_points

def __coordinateList(POIs):
    coords = []

    for i, pt in enumerate(POIs):
        x, y = pt[0]-40, pt[1]-40
        coords.append((x, y))

    return coords

def __filter(POIs, probabilities, min):
    return np.array([(proba, pt) for proba, pt in list(zip(probabilities, POIs)) if proba >= min])

def __scores(scoreRings, points):
    points = np.insert(points, 2, 0, axis=1)
    for i, pt in enumerate(points):
        score = 0
        for j, ring in enumerate(scoreRings.childItems()):
            if j > 0:
                point = QPoint(pt[1][0]+40, pt[1][1]+40)
                if ring.contains(point):
                    score = ring.score
                else:
                    break
        points[i][2] = score
    return points
    
