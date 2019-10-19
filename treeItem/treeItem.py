from ntpath import basename

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from pyexiv2 import Image
import json

from treeItem.hitPointDetector import createHitPointDetector as detectHitPoints
from treeItem.scoreRingDetector import \
    createScoreRingDetector as detectScoreRings
from treeItem.scoreRingDetector import \
    createScoreRingSimulator as simulateScoreRings
from treeItem.targetDetector import createTargetDetector as detectTarget


class TreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, path):
        super(TreeItem, self).__init__(parent)
        super(TreeItem, self).setText(0, "{}".format(basename(path)))
        super(TreeItem, self).setIcon(0, QtGui.QIcon(":/Object/resources/icons8-image-file-80.png"))

        self.QPixmapItem = QPixmapItem(path)
        self.hasRun = False
        self.fileName = path
        self.saved = False

        image = Image(path)
        try:
            self.metadata = json.loads(image.read_exif()['Exif.Photo.UserComment']) 
        except:
            self.metadata = None

    def loadMetadata(self):
        self.saved = False
        for hitPoint in self.metadata['HitPoints'].values():
            self.QPixmapItem.addItem(
                location=QtCore.QPointF(hitPoint['location'][0], hitPoint['location'][1]), 
                score=hitPoint['score'],
                parent=self.QPixmapItem.ConfirmedHitPoints,
                probability=1,
                isHit=True 
                )

        for falsePositive in self.metadata['FalsePositives'].values():
            self.QPixmapItem.addItem(
                location=QtCore.QPointF(falsePositive['location'][0], falsePositive['location'][1]),
                score=hitPoint['score'],
                parent=self.QPixmapItem.HitPoints,
                probability=0,
                isHit=True
                )

        for scoreRing in self.metadata['ScoreRings'].values():
            self.QPixmapItem.addItem(
                location=QtCore.QPointF(scoreRing['location'][0], scoreRing['location'][1]),
                size=scoreRing['size'],
                score=scoreRing['score'],
                angle=scoreRing['angle'],
                parent=self.QPixmapItem.ScoreRings,
                isHit=False
                )
            
    def writeMetadata(self, fileName):
        self.saved = False
        metaImage = Image(fileName)
        data = {
            'Timestamp': metaImage.read_exif()['Exif.Image.DateTime'] if 'Exif.Image.DateTime' in metaImage.read_exif() else '0:0:0 00:00:00', 
            'TotalScore': sum([hitPoint.score for hitPoint in self.QPixmapItem.ConfirmedHitPoints.childItems()]),
            'HitPoints': {
                'Hit{}'.format(i): {
                    'location': (hitPoint.pos().x()+40, hitPoint.pos().y()+40), 
                    'score': hitPoint.score
                    } for i, hitPoint in enumerate(self.QPixmapItem.ConfirmedHitPoints.childItems())
                }, 
            'FalsePositives': {
                'FalsePositive{}'.format(i): {
                    'location': (falsePositive.pos().x()+40, falsePositive.pos().y()+40),
                    'score': falsePositive.score
                    } for i, falsePositive in enumerate(self.QPixmapItem.HitPoints.childItems())
                },
            'ScoreRings': {
                'ScoreRing{}'.format(i): {
                    'location': (scoreRing.pos().x(), scoreRing.pos().y()),
                    'size': (scoreRing.rect().width(), scoreRing.rect().height()),
                    'angle': scoreRing.angle,
                    'score': scoreRing.score
                    } for i, scoreRing in enumerate(self.QPixmapItem.ScoreRings.childItems())
                }
            }

        metaImage.modify_exif({'Exif.Photo.UserComment': json.dumps(data)})

    def addItem(self, *args, **kwargs):
        self.saved = False
        self.QPixmapItem.addItem(*args, **kwargs)

    def run(self):
        if not self.hasRun and self.metadata is None:
            self.saved = False
            self.QPixmapItem.run()
            self.hasRun = True

class QPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, path):
        QPixmap = QtGui.QPixmap(path)
        super(QPixmapItem, self).__init__(QPixmap)
        super(QPixmapItem, self).setTransformationMode(QtCore.Qt.SmoothTransformation)
        
        self.HitPoints = QtWidgets.QGraphicsRectItem(parent=self)
        self.ConfirmedHitPoints = QtWidgets.QGraphicsRectItem(parent=self)
        self.BoundingRect = QtWidgets.QGraphicsRectItem(parent=self)
        self.ScoreRings = QtWidgets.QGraphicsRectItem()

        self.__matImage = cv2.imread(path)
        cv2.cvtColor(self.__matImage, cv2.COLOR_BGR2RGB, self.__matImage)
        self.__matPrimary = self.__matImage.copy()

        pen = QtGui.QPen(QtGui.QColor("blue"))
        pen.setWidth(3)
        self.BoundingRect.setPen(pen)

        self.BoundingRect.setEnabled(False)
        self.ScoreRings.setEnabled(False)

        super(QPixmapItem, self).setVisible(False)
        self.HitPoints.setVisible(False)
        self.ConfirmedHitPoints.setVisible(True)
        self.BoundingRect.setVisible(False)
        self.ScoreRings.setVisible(False)

    def run(self):
        cv_Bullseye = self._detectTarget()
        self._detectScoreRings(cv_Bullseye)
        self._detectHitPoints()

    def addItem(self, *args, **kwargs):
        size = kwargs.get('size') if 'size' in kwargs else (80, 80)
        angle = kwargs.get('angle') if 'angle' in kwargs else 0
        location = kwargs.get('location') if 'location' in kwargs else (0, 0)
        parent = kwargs.get('parent') if 'parent' in kwargs else None
        score = kwargs.get('score') if 'score' in kwargs else 0
        probability = kwargs.get('probability') if 'probability' in kwargs else 0
        isHit = kwargs.get('isHit') if 'isHit' in kwargs else False

        if isHit:
            item = GraphicsItem(size=size, angle=angle, parent=parent, score=score, probability=probability)
            item.confirmed = True if probability == 1 else False
            item.setPos(location - QtCore.QPointF(40, 40))
            item.setFlags(item.ItemIsMovable | item.ItemIsSelectable | item.ItemIsFocusable)
            if score == 0:
                item.setScore()

            self.BoundingRect.setRect(self.HitPoints.childrenBoundingRect() | self.ConfirmedHitPoints.childrenBoundingRect())

        else:            
            item = GraphicsItem(size=size, angle=angle, location=(location.x(), location.y()), parent=parent, score=score, probability=probability)
        
    def _detectTarget(self):
        self.__matImage, cvBullseye = detectTarget(self.__matPrimary.copy())
        
        QImage = QtGui.QImage(
            self.__matImage.data, 
            np.size(self.__matImage, 1), 
            np.size(self.__matImage, 0), 
            self.__matImage.strides[0], 
            QtGui.QImage.Format_RGB888
        )

        QPixmap = QtGui.QPixmap.fromImage(QImage)
        super(QPixmapItem, self).setPixmap(QPixmap)
        super(QPixmapItem, self).setTransformationMode(QtCore.Qt.SmoothTransformation)

        return cvBullseye

    def _detectScoreRings(self, cvBullseye):
        try:
            scoreRings = detectScoreRings(self.__matImage.copy(), cvBullseye)
            self.__updateScoreRingCollection(scoreRings, cvBullseye)

            if self.__detectionFailed() is True:
                print("Detection failed, score rings are simulated")
                raise
        except:
            scoreRings = simulateScoreRings(cvBullseye)
            self.__updateScoreRingCollection(scoreRings, cvBullseye)

    def _detectHitPoints(self):
        hitPoints = detectHitPoints(self.__matImage.copy(), self.ScoreRings)

        for index, (proba, (x, y), score) in enumerate(hitPoints):
            hitPoint = GraphicsItem(score=score, probability=proba, parent=self.HitPoints)
            hitPoint.setPos(x, y)
            hitPoint.setFlags(hitPoint.ItemIsMovable | hitPoint.ItemIsSelectable | hitPoint.ItemIsFocusable)
    
        self.BoundingRect.setRect(self.HitPoints.childrenBoundingRect())

    def __updateScoreRingCollection(self, scoreRings, cvBullseye):
        GraphicsItem(location=cvBullseye[0], size=(1, 1), parent=self.ScoreRings)

        for score, (location, size, angle) in enumerate(scoreRings):
            location = location[0] - (size[0]/2), location[1] - (size[1]/2)
            if score < 10:
                GraphicsItem(location=location, size=size, angle=angle, score=score+1, parent=self.ScoreRings)
            elif score == 10:
                GraphicsItem(location=location, size=size, angle=angle, score=score, parent=self.ScoreRings)

        self.ScoreRings.setEnabled(False)

    def __detectionFailed(self):
        origin = self.ScoreRings.childItems()[0]
        sizes = [(scoreRing.boundingRect().width(), scoreRing.boundingRect().height()) for scoreRing in self.ScoreRings.childItems()]
        
        # Check aspect ratio
        aspectRatios = []
        for i, current in enumerate(sizes):
            if i == 0:
                continue

            previous = sizes[i-1]
            prevW, prevH = previous
            currW, currH = current
            aspectRatios.append(prevW*currH/currW)

        for i, size in enumerate(sizes):
            if i == len(aspectRatios):
                continue

            correctness = size[1] - aspectRatios[i]
            if abs(correctness) > 300:
                return True

        return False

class GraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, *args, **kwargs):
        size = kwargs.get('size') if 'size' in kwargs else (80, 80)
        location = kwargs.get('location') if 'location' in kwargs else (0, 0)
        parent = parent=kwargs.get('parent') if 'parent' in kwargs else None
        self.angle = kwargs.get('angle') if 'angle' in kwargs else 0
        self.score = kwargs.get('score') if 'score' in kwargs else 0
        self.probability = kwargs.get('probability') if 'probability' in kwargs else 0
        self.confirmed = False
        self.moved = False
        
        penRed = QtGui.QPen(QtGui.QColor(255, 0, 0))
        penRed.setWidth(5)
        penYellow = QtGui.QPen(QtGui.QColor(255, 255, 0))
        penYellow.setWidth(5)
        penBlue = QtGui.QPen(QtGui.QColor(0, 0, 255))
        penBlue.setWidth(5)
        penGreen = QtGui.QPen(QtGui.QColor(0, 255, 0))
        penGreen.setWidth(5)

        super(GraphicsItem, self).__init__(location[0], location[1], size[0], size[1], parent)
        super(GraphicsItem, self).setStartAngle(self.angle)

        if self.probability == 0:
            super(GraphicsItem, self).setPen(penBlue)
        elif self.probability > 0 and self.probability < 0.85:
            super(GraphicsItem, self).setPen(penRed)
        elif self.probability >= 0.85 and self.probability < 1:
            super(GraphicsItem, self).setPen(penYellow)
        elif self.probability == 1:
            super(GraphicsItem, self).setPen(penGreen)

    def setScore(self, newScore=None):
        score = 0
        if newScore is not None:
            score = newScore

        else:
            for j, ring in enumerate(self.parentItem().parentItem().ScoreRings.childItems()):
                if j > 0:
                    point = QtCore.QPoint( super(GraphicsItem, self).pos().x()+40, super(GraphicsItem, self).pos().y()+40 )
                    if ring.contains(point):
                        score = ring.score
                    else:
                        break
        self.score = score

    def paint(self, painter, option, widget):
        if self.confirmed:
            pen = QtGui.QPen(QtGui.QColor(0, 200, 0))
            pen.setWidth(5)
            super(GraphicsItem, self).setPen(pen)

            self.probability = 1
            super(GraphicsItem, self).setParentItem(super(GraphicsItem, self).parentItem().parentItem().ConfirmedHitPoints)

        super(GraphicsItem, self).paint(painter, option, widget)

    def mouseReleaseEvent(self, event):
        if self.moved:
            self.setScore()
            self.moved = False
        super(GraphicsItem, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.moved = True
        super(GraphicsItem, self).mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.confirmed = True
        self.update()
        super(GraphicsItem, self).mouseDoubleClickEvent(event)
