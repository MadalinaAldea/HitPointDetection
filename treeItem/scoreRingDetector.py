from treeItem.lineIterator import createLineIterator
from treeItem.lineIterator import createLineIterator as create_line

import cv2
import numpy as np
from matplotlib import pyplot as plt

def createScoreRingDetector(src, bullseye):
    cv2.cvtColor(src, cv2.COLOR_RGB2BGR, src)

    outerScoreRings = __outerRings(src, bullseye)
    innerScoreRings = __innerRings(bullseye)
    scoreRings = outerScoreRings + innerScoreRings

    return scoreRings
    
def createScoreRingSimulator(bullseye):
    bOrigo, bSize, bAngle = bullseye
    size = list(__mm(bSize, 25, 25))
    width = __mm(bSize, 25, 25)
    score = 10
    
    ellipses = []
    ellipses.append((bOrigo, size, bAngle))
    size = list(__mm(bSize, 50, 50))
    
    for _ in range(11):
        ellipses.append((bOrigo, size.copy(), bAngle))

        for i, meas in enumerate(__mm(bSize, 50, 50)):
            size[i] += meas
        score -= 1
        width = __mm(bSize, 50, 50)

    ellipses.sort(key=lambda x: x[1][0], reverse=True)
    
    return ellipses

def __outerRings(src, bullseye):
    # Hitta poängringar utanför riktpricken och returnera en lista med ring 1-6
    height, width, _ = src.shape
    origo = tuple(map(int, bullseye[0]))

    roi = __regionOfInterest(src, bullseye)
    bil_filt = cv2.bilateralFilter(roi, 5, 150, 150)
    gray = cv2.cvtColor(bil_filt, cv2.COLOR_BGR2GRAY)
    cnts_mask = np.zeros_like(gray)


    # Threshhold process
    blocksize = int(height/30)
    if blocksize % 2 == 0:
        blocksize += 1
    C = blocksize/4
    mean = np.mean(gray[np.nonzero(gray)])
    shape = (5,5)
    if mean >= 190:
        shape = (7,7)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, shape)

    adp_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blocksize, C)
    fg_thresh = cv2.morphologyEx(adp_thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    comp_thresh = cv2.compare(adp_thresh, fg_thresh, cv2.CMP_GT)
    cv2.line(comp_thresh, origo, (0,0), 0, 10)
    
    # Find most significant contours
    cnts = cv2.findContours(comp_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    cnts.sort(key=lambda x: cv2.arcLength(x, False), reverse=True)
    index = np.max(np.where(np.array([cv2.arcLength(cnts[i], False) for i in range(len(cnts))]) > 300))
    cnts = cnts[0:int(index)]
    # Is contour bad?
    ring_cnts = []
    for i in range(len(cnts)):
        if not __contourIsStraight(cnts[i]):
            ring_cnts.append(cnts[i])
    cnts = ring_cnts
    cv2.drawContours(cnts_mask, cnts, -1, 255, -1)

    # Draw Lines from origo to img edges in anti-clockwise order
    lines = []
    inc_h = int(height/30)
    inc_w = int(width/30)

    for j in range(30): # Left side top to bottom
        line = create_line(origo, np.array([0, j*inc_h]), cnts_mask)
        lines.append(line)
    
    for j in range(30): # Bottom side left to right
        line = create_line(origo, np.array([j*inc_w, height]), cnts_mask)
        lines.append(line)

    for j in range(30, 0, -1):  # Right side bottom to top
        line = create_line(origo, np.array([width, j*inc_h]), cnts_mask)
        lines.append(line)

    for j in range(30, 0, -1): # Top side right to left
        line = create_line(origo, np.array([j*inc_w, 0]), cnts_mask)
        lines.append(line)

    # Find points where the lines intersects the contours            
    intersections = []
    intersections.append([np.where([i[2]==255 for i in line]) for line in lines])
    intersections = [point[0] for point in intersections[0]]

    # Save one point per line match
    avg_diff = __averageDiff(intersections)
    diff = [np.where(np.diff(points) <= avg_diff) for points in intersections]
    for i, j in enumerate(diff):
        intersections[i] = np.delete(intersections[i], j)
    
    # Save lines with 6 intersections and save those intersection-indexes and lines
    indexes = np.where([len(cs) == 6 for cs in intersections])[0]
    intersections = [intersections[i] for i in indexes]
    lines = [lines[i] for i in indexes]

    # Save only 'match-point-coordinates' in lines
    for i in range(len(lines)):
        lines[i] = [lines[i][j] for j in intersections[i]]

    # Turn lines into pure coordinates (remove point intensities)
    lines = [np.delete(line, 2, 1) for line in lines]
    lines = np.asarray(lines)
    
    # Rearrange 'match-point-coordinates' arranged by score line
    rings = np.transpose(lines, (1,0,2))

    # Find the contour indexes that the lines intersect and sort matches by score line-layer
    contours = [[],[],[],[],[],[]]
    for layer, ring in enumerate(rings):
        for pt in ring:
            for i, cnt in enumerate(cnts):
                point_pos = cv2.pointPolygonTest(cnt, tuple(pt), False)
                if point_pos >= 0 and i not in contours[layer]:
                    contours[layer].append(i)

    # Find the actual contours
    for l, layer in enumerate(contours):
        for i, ind in enumerate(layer):
            contours[l][i] = cnts[ind]
    
    # Fit ellipse inside the contours
    ring = np.zeros_like(bil_filt)
    hull = [__convexHull(contours[i]) for i in range(len(contours))]
    [cv2.drawContours(ring, contours[i], -1, (255,255,255), -1) for i in range(len(contours))]
    ellipses = [cv2.fitEllipse(hull[i]) for i in range(len(hull))]
    ellipses.sort(key=lambda x: x[1][0], reverse=True)

    return ellipses

def __innerRings(bullseye):
    bOrigo, bSize, bAngle = bullseye
    size = list(__mm(bSize, 25, 25))
    width = __mm(bSize, 25, 25)
    score = 10
    
    ellipses = []
    ellipses.append((bOrigo, size, bAngle))
    
    size = list(__mm(bSize, 50, 50))
    
    for _ in range(4):
        ellipses.append((bOrigo, size.copy(), bAngle))

        for i, meas in enumerate(__mm(bSize, 50, 50)):
            size[i] += meas
        score -= 1
        width = __mm(bSize, 50, 50)

    ellipses.sort(key=lambda x: x[1][0], reverse=True)
    
    return ellipses

def __averageDiff(intersections):
    dist = [np.diff(points) for points in intersections]
    dist = [list(dist[i][np.where(dist[i] > 1)]) for i in range(len(dist))]
    dist = np.asarray([val for sublist in dist for val in sublist])

    dist_hist = np.bincount(dist)

    diff = np.where(dist_hist >= 3)[0]
    diff = diff[np.where(diff > 20)][0]

    return diff  

def __mm(bSize, width, height):
    w, h = bSize
    w = w / 200 * width
    h = h / 200 * height

    return w, h

def __contourIsStraight(cnt):
    peri = cv2.arcLength(cnt, False)
    approx = cv2.approxPolyDP(cnt, 0.01*peri, False)
    length = len(approx)

    return length <= 4

def __regionOfInterest(src, bullseye):
    mask = np.zeros_like(src)
    bOrigo, (bWidth, bHeight), bAngle = bullseye
    roi = (bOrigo, (bWidth*1.1, bHeight*1.1), bAngle)

    cv2.ellipse(mask, roi, (255, 255, 255), -1)
    mask = cv2.bitwise_not(mask)
    masked_image = cv2.bitwise_and(src, mask)

    return masked_image

def __convexHull(contours):
    pts = []

    for i in range(len(contours)):
        for j in range(len(contours[i])):
            pts.append(contours[i][j])

    pts = np.asarray(pts)
    pts = cv2.convexHull(pts)

    return pts

    