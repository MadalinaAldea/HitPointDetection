import cv2
import numpy as np
from treeItem.bullseyeDetector import createBullseyeDetector as detectBullseye

def createTargetDetector(src):
    cv2.cvtColor(src, cv2.COLOR_RGB2BGR, src)

    morph = __morphTarget(src)
    contour = __targetContour(morph)

    x, y, w, h = cv2.boundingRect(contour)
    target = src[y:y+h, x:x+w]
    roi, bullseye = __regionOfInterest(target)

    cv2.cvtColor(roi, cv2.COLOR_BGR2RGB, roi)

    return roi, bullseye

def __morphTarget(src):
    kernel = np.ones((15, 15), np.uint8)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    return closing

def __targetContour(src):
    contours = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    max_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.01*cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)

    return approx

def __regionOfInterest(src):
    bullseye = detectBullseye(src)
    mask = np.zeros_like(src)

    roi = (bullseye[0], (bullseye[1][0]*2.8, bullseye[1][1]*2.8), bullseye[2])

    cv2.ellipse(mask, roi, (255, 255, 255), -1)
    targetROI = cv2.bitwise_and(src, mask)

    return targetROI, bullseye