import cv2
from skimage import feature
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np

def predict(src, coords):
    POIs = __predData(src, coords)
    predictions = __predictHit(POIs)
    return predictions

def __predData(src, coords):
    POIs = []

    for pt in coords:
        (x, y) = pt
        POI = src[y:y+80, x:x+80]

        median = cv2.medianBlur(POI, 5)
        canny = cv2.Canny(median, 100, 200)
        HOG = feature.hog(canny,
                          orientations=12,
                          pixels_per_cell=(8,8),
                          cells_per_block=(3,3),
                          transform_sqrt=True,
                          block_norm='L1')
        POIs.append(HOG)

    for i in range(len(POIs)):
        while POIs[i].shape[0] != 6912:
            POIs[i] = np.append(POIs[i], 0.0)

    return POIs

def __predictHit(POIs):
    svm = joblib.load("treeItem/data/svm_model.sav")
    scaler = StandardScaler()
    scaledPredData = scaler.fit_transform(POIs)
    probabilities = svm.predict_proba(scaledPredData)

    return probabilities


