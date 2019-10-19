import numpy as np
from skimage import exposure, feature
from sklearn import preprocessing, svm
from sklearn.externals import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils import shuffle


def __update_train_HOG() -> None:
    """ Generate new train data from pre-defined POIs.

    To create pre-defined POIs:
        1. Generate POIs with hough circle transform and crop (80x80) fragments
        2. Divide set of POIs into train and test data-sets 
        3. Divide each data-set into hit (pos) and no-hit (neg)
           In folders:
               /treeItem/data/train/pos    <-- insert positive training image fragments (80x80 pixles each)
               /treeItem/data/train/neg    <-- insert negative training image fragments (80x80 pixles each)
               /treeItem/data/test/pos     <-- insert positive testing image fragments (80x80 pixles each)
               /treeItem/data/test/neg     <-- insert negative testing image fragments (80x80 pixles each)
    """
    uppder_dir = ['train', 'test']
    lower_dir = ['neg', 'pos']

    train = [[],[]]
    test = [[],[]]
    img_list = train, test

    for i, ttDir in enumerate(uppder_dir):
        ttPath = 'treeItem/data/train/{}'.format(ttDir)

        for j, binDir in enumerate(lower_dir):
            binPath = ttPath + '/{}'.format(binDir)

            for pt in [f for f in os.listdir(binPath) if os.path.isfile(os.path.join(binPath, f))]:
                point_img = cv2.imread(binPath + '/{}'.format(pt))
                median = cv2.medianBlur(point_img, 5)
                canny = cv2.Canny(median, 100, 200)
                HOG = feature.hog(canny, 
                                  orientations=12, 
                                  pixels_per_cell=(8,8),
                                  cells_per_block=(3,3), 
                                  transform_sqrt=True, 
                                  block_norm='L1')
                img_list[i][j].append(HOG)

    np.save('treeItem/data/train/train_data.npy', train)
    np.save('treeItem/data/train/test_data.npy', test)

def __unused_TrainModel(self, negTrain, posTrain, negTest, posTest):
    negTrain_lbl = np.zeros(len(negTrain)).astype(int)
    posTrain_lbl = np.ones(len(posTrain)).astype(int)
    negTest_lbl = np.zeros(len(negTest)).astype(int)
    posTest_lbl = np.ones(len(posTest)).astype(int)

    XTest = np.concatenate((negTest, posTest), axis=0)
    yTest = np.concatenate((negTest_lbl, posTest_lbl), axis=0)

    XTrain = np.concatenate((negTrain, posTrain), axis=0)
    yTrain = np.concatenate((negTrain_lbl, posTrain_lbl), axis=0)

    shuffle(XTrain, yTrain)
    
    encoder = preprocessing.LabelEncoder()
    encoder.fit(yTrain)
    encoder.fit(yTest)
    YTrain = encoder.fit_transform(yTrain)
    YTest = encoder.fit_transform(yTest)

    scaler = StandardScaler()
    XTrain_scaled = scaler.fit_transform(XTrain)
    XTest_scaled = scaler.fit_transform(XTest)

    paramsGrid = [{'kernel': ['rbf'], 'gamma': [1e-1, 1e-2, 1e-3, 1e-4], 
                    'C': [1, 10, 100, 1000]},
                   {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    svc = SVC(probability=True)
    tempModel = GridSearchCV(svc, paramsGrid, cv=5)
    tempModel.fit(XTrain_scaled, YTrain)

    print('Best score for training data: ', tempModel.best_score_, '\n')
    print('Best C: ', tempModel.best_estimator_.C, '\n')
    print('Best Kernel: ', tempModel.best_estimator_.kernel, '\n')
    print('Best Gamma: ', tempModel.best_estimator_.gamma, '\n')

    finalModel = tempModel.best_estimator_
    YPred = finalModel.predict(XTest_scaled)
    YPred_label = list(encoder.inverse_transform(YPred))
    
    print(confusion_matrix(yTest, YPred_label))
    print('\n')
    print(classification_report(yTest, YPred_label))
    print('Training set score for SVM: %f' % finalModel.score(XTrain_scaled, yTrain))
    print('Testing set score for SVM: %f' % finalModel.score(XTest_scaled, yTest))

    filename = 'treeItem/data/train/svm_model.sav'
    joblib.dump(finalModel, filename)
