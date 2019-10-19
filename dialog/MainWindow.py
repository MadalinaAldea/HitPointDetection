# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
""" Created by: PyQt5 UI code generator 5.13.0

 WARNING! All changes made in this file will be lost!"""

from ntpath import basename, dirname, join

from PyQt5 import QtCore, QtGui, QtWidgets

import dialog.rsc
from dialog.ExitWithoutSave import UiExitWithoutSave
from treeItem.treeItem import GraphicsItem, TreeItem


class UiMainWindow(QtWidgets.QMainWindow):
    """Class string"""
    def __init__(self, parent=None):
        super(UiMainWindow, self).__init__()
        self.setupUi(parent)

    def onZoomInClicked(self) -> None:
        """ Scale up QGraphicsView
        """
        try:
            if self.QView.transform().m11() < self.QViewScaleMax:
                self.QView.scale(self.QViewScaleFactor, self.QViewScaleFactor)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onZoomOutClicked(self) -> None:
        """ Scale down QGraphicsView
        """
        try:
            if self.QView.transform().m11() >= self.QViewScaleMin:
                self.QView.scale(1/self.QViewScaleFactor, 1/self.QViewScaleFactor)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onRstZoomClicked(self) -> None:
        """ Reset QGraphicsView scale to original
        """
        try:
            self.QView.setTransform(self.QViewTransform)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onSelectClicked(self, checked) -> None:
        """ Enable QGraphicsView select mode
        """
        try:
            self.QView.setDragMode(self.QView.NoDrag)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onMoveClicked(self, checked) -> None:
        """ Enable QGraphicsView move mode
        """
        try:
            self.QView.setDragMode(self.QView.ScrollHandDrag)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onHitPointsChecked(self, checked) -> None:
        """ Show/Hide hitpoints button logic
        """
        try:
            self.Item.QPixmapItem.HitPoints.setVisible(checked)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onEnclosingChecked(self, checked) -> None:
        """ Show/Hide enclosing rectangle button logic
        """
        try:
            self.Item.QPixmapItem.BoundingRect.setVisible(checked)            
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onAddTriggered(self) -> None:
        """ If Hit Point item selected:
                Validate Hit Point
            Else:
                Add new Hit Point on last view key press location
        """
        try:
            if self.QScene.selectedItems():
                for item in self.QScene.selectedItems():
                    item.confirmed = True
                    item.update()
            else:
                self.Item.addItem(location=self.QScene.mousePressPos(), parent=self.Item.QPixmapItem.ConfirmedHitPoints, isHit=True, probability=1)

        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onDeleteTriggered(self) -> None:
        """ If Hit Point selected:
                Delete selected Hit Point
            Else if Image (Tree item) selected:
                Delete selected Image (Tree Item)
        """
        try:
            if len(self.QScene.selectedItems()) > 0:
                [self.QScene.removeItem(item) for item in self.QScene.selectedItems()]
            else:
                index = self.QTree.indexOfTopLevelItem(self.Item)
                next = self.QTree.topLevelItem(index+1) if self.QTree.topLevelItem(index+1) is not None else self.QTree.topLevelItem(index-1)

                self.QTree.takeTopLevelItem(index)
                self.QScene.removeItem(self.Item.QPixmapItem)
                self.onTreeItemClicked(next, 0) if next else self.QScene.clear()
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onEditTriggered(self) -> None:
        """ Edit selected Hit Point score value
        """
        try:
            for item in self.QScene.selectedItems():
                score, ok = QtWidgets.QInputDialog.getInt(self, "Edit Score", "Score: ", item.score, 0, 10, 1)
                if ok:
                    item.setScore(score)
                    self.Item.saved = False
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onSaveTriggered(self) -> None:
        """ If current image (Tree Item) has been saved before:
                Save current Image as its current file name (Tree Item)
            Else:
                Goto Save as...
        """
        try:
            if not self.Item.saved:
                self.onSaveAsTriggered()
            else:
                self.Item.QPixmapItem.pixmap().save(self.Item.fileName)
                self.Item.writeMetadata(self.Item.fileName)
                self.Item.saved = True
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")
    
    def onSaveAsTriggered(self) -> None:
        """ Save current Image (Tree Item) as <fileName>
        """
        try:
            options = QtWidgets.QFileDialog.Options()
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, 
                                                                'Save Target Project', 
                                                                '', 
                                                                'Image (*.jpg *.jpeg *.png *.bmp)',
                                                                options=options)
            if fileName:
                self.Item.QPixmapItem.pixmap().save(fileName)
                self.Item.writeMetadata(fileName)
                self.Item.saved = True
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")
    
    def onSaveAllTriggered(self) -> None:
        """ Save all images in list
        """
        try:
            for i in range(self.QTree.topLevelItemCount()):
                item = self.QTree.topLevelItem(i)
                item.QPixmapItem.pixmap().save(item.fileName)
                item.writeMetadata(item.fileName)
                item.saved = True
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onSaveDataPointsTriggered(self) -> None:
        """ Edit selected Hit Point
        """
        try:
            pass
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onSaveHitPointsTriggered(self) -> None:
        """ Edit selected Hit Point
        """
        try:
            pass
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onSaveFalsePositivesTriggered(self) -> None:
        """ Edit selected Hit Point
        """
        try:
            pass
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onStartTriggered(self) -> None:
        """ Begin automatic hit point detection
        """
        try:
            self.Item.run()
            items = self.QScene.items()
            self.QBtnHitPoints.setChecked(True)
            self.QBtnEnclosing.setChecked(False)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")
    
    def onNewTriggered(self) -> None:
        """ Replace current ImageQue to chosen image(s) and update QTreeWidget
        """
        # -> Open dialog "Close all current images?"
        # -> if OK:
        try:
            options = QtWidgets.QFileDialog.Options()
            fileNames, _ = QtWidgets.QFileDialog().getOpenFileNames(None, 'New Target', '',
                                                                'Images (*.jpg *.jpeg *.png *.bmp)', options=options)
            if fileNames:
                self.QTree.clear()
                self.QScene.clear()
                for fileName in fileNames:
                    if fileName:
                        treeItem = TreeItem(self.QTree, fileName)
                        if treeItem.metadata is not None:
                            treeItem.loadMetadata()                   
                        self.QScene.addItem(treeItem.QPixmapItem)

                item = self.QTree.topLevelItem(0)
                item.setSelected(True)
                self.onTreeItemClicked(item, 0)

                self.QViewTransform = self.QView.transform()
                self.QViewScaleMin = self.QViewTransform.m11() * 0.5
                self.QViewScaleMax = self.QViewTransform.m11() * 5
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def onOpenTriggered(self) -> None:
        """ Add chosen image(s) to current ImageQue and update QTreeWidget
        """
        try:
            options = QtWidgets.QFileDialog.Options()
            fileNames, _ = QtWidgets.QFileDialog().getOpenFileNames(None, 'New Target', '',
                                                                'Images (*.png *.jpeg *.jpg *bmp', options=options)
            if fileNames:
                for fileName in fileNames:
                    itemList = [item.text(0) for item in self.QTree.findItems(basename(fileName), QtCore.Qt.MatchExactly)]
                    if fileName and basename(fileName) not in itemList:
                        treeItem = TreeItem(self.QTree, fileName)
                        if treeItem.metadata is not None:
                            treeItem.loadMetadata()         
                        self.QScene.addItem(treeItem.QPixmapItem)
                if self.Item:
                    self.Item.setSelected(True)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")
    
    def onTreeItemClicked(self, item, column) -> None:
        try:
            self.Item = item

            self.QView.fitInView(self.Item.QPixmapItem, QtCore.Qt.KeepAspectRatioByExpanding)
            
            [self.QTree.topLevelItem(i).QPixmapItem.setVisible(False) for i in range(self.QTree.topLevelItemCount())]
            self.Item.QPixmapItem.setVisible(True)

            self.QBtnHitPoints.setChecked(True) if self.Item.QPixmapItem.HitPoints.isVisible() else self.QBtnHitPoints.setChecked(False)
            self.QBtnEnclosing.setChecked(True) if self.Item.QPixmapItem.BoundingRect.isVisible() else self.QBtnEnclosing.setChecked(False)
        except:
            self.QStatus.showMessage("Status: Wait...")
        else:
            self.QStatus.showMessage("Status: Done")

    def focusItemChanged(self):
        try:
            self.QStatus.showMessage("Status: Score: {}, Location: ({}, {})".format( self.QScene.focusItem().score, 
                                                                                     int(self.QScene.focusItem().pos().x()+40), 
                                                                                     int(self.QScene.focusItem().pos().y()+40) ))
        except:
            self.QStatus.showMessage("Status: Done")

    def setupUi(self, MainWindow) -> None:
        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(530, 376))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Graphics Scene Target Image
        self.QScene = QScene()#Widgets.QGraphicsScene()
        self.QScene.focusItemChanged.connect(self.focusItemChanged)
        
        # Graphics View Target Image
        self.QView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(255)
        sizePolicy.setVerticalStretch(255)
        sizePolicy.setHeightForWidth(self.QView.sizePolicy().hasHeightForWidth())
        self.QView.setSizePolicy(sizePolicy)
        self.QView.setMinimumSize(QtCore.QSize(200, 200))
        self.QView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.QView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.QView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.QView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.QView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.QView.setRenderHints(QtGui.QPainter.TextAntialiasing)
        self.QView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.QView.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.QView.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.QView.viewport().setProperty("cursorSelect", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.QView.viewport().setProperty("cursorMove", QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.QView.setObjectName("view_TargetImage")
        self.QView.setMouseTracking(True)
        self.QView.setInteractive(True)
        self.gridLayout.addWidget(self.QView, 1, 1, 1, 1)
        self.QView.setScene(self.QScene)

        # Independent members
        self.QViewScaleMin = 0.1
        self.QViewScaleMax = 10
        self.QViewScaleFactor = 1.1

        # Push Buttons
        # |_ Zoom in
        self.QBtnZoomIn = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-zoom-in-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnZoomIn.setIcon(icon)
        self.QBtnZoomIn.setAutoRepeat(True)
        self.QBtnZoomIn.setAutoExclusive(True)
        self.QBtnZoomIn.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.QBtnZoomIn.setAutoRaise(True)
        self.QBtnZoomIn.setObjectName("pushButton_ZoomIn")
        self.QBtnZoomIn.clicked.connect(self.onZoomInClicked)
        self.horizontalLayout.addWidget(self.QBtnZoomIn)

        # |_ Zoom Out
        self.QBtnZoomOut = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-zoom-out-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnZoomOut.setIcon(icon)
        self.QBtnZoomOut.setAutoRepeat(True)
        self.QBtnZoomOut.setAutoExclusive(True)
        self.QBtnZoomOut.setAutoRaise(True)
        self.QBtnZoomOut.setObjectName("pushButton_ZoomOut")
        self.QBtnZoomOut.clicked.connect(self.onZoomOutClicked)
        self.horizontalLayout.addWidget(self.QBtnZoomOut)

        # |_ Reset Zoom
        self.QBtnZoomRst = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-zoom-to-actual-size-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnZoomRst.setIcon(icon)
        self.QBtnZoomRst.setAutoExclusive(True)
        self.QBtnZoomRst.setAutoRaise(True)
        self.QBtnZoomRst.setObjectName("pushButton_ResetZoom")
        self.QBtnZoomRst.clicked.connect(self.onRstZoomClicked)
        self.horizontalLayout.addWidget(self.QBtnZoomRst)

        # |_ Select
        self.QBtnSelect = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-cursor-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnSelect.setIcon(icon)
        self.QBtnSelect.setCheckable(True)
        self.QBtnSelect.setAutoExclusive(True)
        self.QBtnSelect.setAutoRaise(True)
        self.QBtnSelect.setObjectName("pushButton_Select")
        self.QBtnSelect.toggled.connect(self.onSelectClicked)
        self.horizontalLayout.addWidget(self.QBtnSelect)

        # |_ Move
        self.QBtnMove = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-move-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnMove.setIcon(icon)
        self.QBtnMove.setCheckable(True)
        self.QBtnMove.setChecked(True)
        self.QBtnMove.setAutoExclusive(True)
        self.QBtnMove.setAutoRaise(True)
        self.QBtnMove.setObjectName("pushButton_Move")
        self.QBtnMove.toggled.connect(self.onMoveClicked)
        self.horizontalLayout.addWidget(self.QBtnMove)

        # |_ Spacer Item
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        # |_ Hit Points
        self.QBtnHitPoints = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-hunt-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnHitPoints.setIcon(icon6)
        self.QBtnHitPoints.setCheckable(True)
        self.QBtnHitPoints.setAutoRaise(True)
        self.QBtnHitPoints.setObjectName("QBtnHitPoints")
        self.QBtnHitPoints.toggled.connect(self.onHitPointsChecked)
        self.horizontalLayout.addWidget(self.QBtnHitPoints)

        # |_ Enclosing Ellipse
        self.QBtnEnclosing = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Image/resources/icons8-polygon-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QBtnEnclosing.setIcon(icon7)
        self.QBtnEnclosing.setCheckable(True)
        self.QBtnEnclosing.setAutoRaise(True)
        self.QBtnEnclosing.setObjectName("QBtnEnclosing")
        self.QBtnEnclosing.toggled.connect(self.onEnclosingChecked)
        self.horizontalLayout.addWidget(self.QBtnEnclosing)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        # Tree Hit Points
        self.QTree = QtWidgets.QTreeWidget(self.centralwidget)
        self.QTree.setMinimumSize(QtCore.QSize(100, 200))
        self.QTree.setMaximumSize(QtCore.QSize(300, 16777215))
        self.QTree.setInputMethodHints(QtCore.Qt.ImhNone)
        self.QTree.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.QTree.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.QTree.setDragEnabled(True)
        self.QTree.setObjectName("tree_HitPoints")
        self.QTree.header().setStretchLastSection(True)
        self.gridLayout.addWidget(self.QTree, 1, 0, 1, 1)
        self.QTree.itemClicked.connect(self.onTreeItemClicked)

        # Menu Bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.QMenu = QtWidgets.QMenuBar(MainWindow)
        self.QMenu.setGeometry(QtCore.QRect(0, 0, 1000, 18))
        self.QMenu.setObjectName("menubar")

        # |_ File
        self.QMenuFile = QtWidgets.QMenu(self.QMenu)
        self.QMenuFile.setObjectName("Menu")

        # |_ Edit
        self.QMenuEdit = QtWidgets.QMenu(self.QMenu)
        self.QMenuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.QMenu)

        # |_ Status Bar
        self.QStatus = QtWidgets.QStatusBar(MainWindow)
        self.QStatus.setObjectName("statusbar")
        self.QScene.statusbar = self.QStatus
        self.QStatus.showMessage("Status: Ready")
        MainWindow.setStatusBar(self.QStatus)

        # |_ Tool Bar
        self.QToolBar = QtWidgets.QToolBar(MainWindow)
        self.QToolBar.setEnabled(True)
        self.QToolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.QToolBar)

        # Actions
        # |_ New
        self.QNew = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-file-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QNew.setIcon(icon)
        self.QNew.setObjectName("actionNew")
        self.QNew.triggered.connect(self.onNewTriggered)

        # |_ Open
        self.QOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-opened-folder-50-3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QOpen.setIcon(icon)
        self.QOpen.setObjectName("actionOpen")
        self.QOpen.triggered.connect(self.onOpenTriggered)

        # |_ Save
        self.QSave = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-save-50-4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QSave.setIcon(icon)
        self.QSave.setObjectName("actionSave")
        self.QSave.triggered.connect(self.onSaveTriggered)

        # |_ Save As
        self.QSaveAs = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-save-as-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QSaveAs.setIcon(icon)
        self.QSaveAs.setObjectName("actionSave_As")
        self.QSaveAs.triggered.connect(self.onSaveAsTriggered)

        # |_ Save All
        self.QSaveAll = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-save-all-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QSaveAll.setIcon(icon)
        self.QSaveAll.setObjectName("actionSave_All")
        self.QSaveAll.triggered.connect(self.onSaveAllTriggered)
        
        # |_ Save All Datapoints 
        self.QSaveDataPoints = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-pictures-folder-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QSaveDataPoints.setIcon(icon)
        self.QSaveDataPoints.setObjectName("actionSave_DataPoints")
        self.QSaveDataPoints.triggered.connect(self.onSaveDataPointsTriggered)

        # |_ Save Hit Points
        self.QSaveHitPoints = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-pictures-folder-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QSaveHitPoints.setIcon(icon)
        self.QSaveHitPoints.setObjectName("actionSave_HitPoints")
        self.QSaveHitPoints.triggered.connect(self.onSaveHitPointsTriggered)

        # |_ Save False positives
        self.QSaveFalsePositives = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/File/resources/icons8-pictures-folder-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QSaveFalsePositives.setIcon(icon)
        self.QSaveFalsePositives.setObjectName("actionSave_FalsePositives")
        self.QSaveFalsePositives.triggered.connect(self.onSaveFalsePositivesTriggered)

        # |_ Add
        self.QAdd = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Object/resources/icons8-add-50-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QAdd.setIcon(icon)
        self.QAdd.setObjectName("actionAdd")
        self.QAdd.triggered.connect(self.onAddTriggered)
        # Disable add from beginning (enable when location on image are selected)

        # |_ Delete
        self.QDelete = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Object/resources/icons8-cancel-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QDelete.setIcon(icon)
        self.QDelete.setObjectName("actionDelete")
        self.QDelete.triggered.connect(self.onDeleteTriggered)
        # Disable delete from beginning (enable when image/HP are selected)

        # |_ Edit
        self.QEdit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Object/resources/icons8-edit-50-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QEdit.setIcon(icon)
        self.QEdit.setObjectName("actionEdit")
        self.QEdit.triggered.connect(self.onEditTriggered)
        # Disable edit from beginning (enable when image/HP are selected)

        # |_ Start
        self.QStart = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Program/resources/icons8-play-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QStart.setIcon(icon)
        self.QStart.setObjectName("actionStart")
        self.QStart.triggered.connect(self.onStartTriggered)

        # Add Actions to Menu
        self.QMenuFile.addAction(self.QNew)
        self.QMenuFile.addAction(self.QOpen)
        self.QMenuFile.addSeparator()
        self.QMenuFile.addAction(self.QSave)
        self.QMenuFile.addAction(self.QSaveAs)
        self.QMenuFile.addAction(self.QSaveAll)
        self.QMenuFile.addSeparator()
        self.QMenuFile.addAction(self.QSaveDataPoints)
        self.QMenuFile.addAction(self.QSaveHitPoints)
        self.QMenuFile.addAction(self.QSaveFalsePositives)

        self.QMenuEdit.addAction(self.QStart)
        self.QMenuEdit.addSeparator()
        self.QMenuEdit.addAction(self.QAdd)
        self.QMenuEdit.addAction(self.QDelete)
        self.QMenu.addAction(self.QMenuFile.menuAction())
        self.QMenu.addAction(self.QMenuEdit.menuAction())

        # Add Actions to toolbar
        self.QToolBar.addAction(self.QAdd)
        self.QToolBar.addAction(self.QDelete)
        self.QToolBar.addAction(self.QEdit)
        self.QToolBar.addAction(self.QStart)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.QBtnMove, self.QTree)
        MainWindow.setTabOrder(self.QTree, self.QView)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # Push Buttons
        # |_ Zoom In
        self.QBtnZoomIn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zoom in (Ctrl+\'+\')</p></body></html>"))
        self.QBtnZoomIn.setText(_translate("MainWindow", "..."))
        self.QBtnZoomIn.setShortcut(_translate("MainWindow", "Ctrl++"))
        # |_ Zoom Out
        self.QBtnZoomOut.setToolTip(_translate("MainWindow", "<html><head/><body><p>Zoom out (Ctrl+\'-\')</p></body></html>"))
        self.QBtnZoomOut.setText(_translate("MainWindow", "..."))
        self.QBtnZoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
        # |_ Zoom Reset
        self.QBtnZoomRst.setToolTip(_translate("MainWindow", "<html><head/><body><p>Reset view (Ctrl+0)</p></body></html>"))
        self.QBtnZoomRst.setText(_translate("MainWindow", "..."))
        self.QBtnZoomRst.setShortcut(_translate("MainWindow", "Ctrl+0"))
        # |_ Select
        self.QBtnSelect.setToolTip(_translate("MainWindow", "<html><head/><body><p>Select (Ctrl+Q)</p></body></html>"))
        self.QBtnSelect.setText(_translate("MainWindow", "..."))
        self.QBtnSelect.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        # |_ Move
        self.QBtnMove.setToolTip(_translate("MainWindow", "<html><head/><body><p>Move (Ctrl+W)</p></body></html>"))
        self.QBtnMove.setText(_translate("MainWindow", "..."))
        self.QBtnMove.setShortcut(_translate("MainWindow", "Ctrl+W"))

        # Tree
        self.QTree.headerItem().setText(0, _translate("MainWindow", "Image"))
        __sortingEnabled = self.QTree.isSortingEnabled()
        self.QTree.setSortingEnabled(False)
        self.QTree.setSortingEnabled(__sortingEnabled)

        # Menu
        self.QMenuFile.setTitle(_translate("MainWindow", "&File"))
        self.QMenuEdit.setTitle(_translate("MainWindow", "Edit"))

        # Toolbar
        self.QToolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

        # Actions
        # |_ Open
        self.QOpen.setText(_translate("MainWindow", "Open..."))
        self.QOpen.setToolTip(_translate("MainWindow", "<html><head/><body><p>Open (Ctrl+O)</p></body></html>"))
        self.QOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        # |_ Save
        self.QSave.setText(_translate("MainWindow", "Save"))
        self.QSave.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save (Ctrl+S)</p></body></html>"))
        self.QSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        # |_ Save as
        self.QSaveAs.setText(_translate("MainWindow", "Save As..."))
        self.QSaveAs.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save As (Ctrl+Shift+S)</p></body></html>"))
        self.QSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        # |_ Save all
        self.QSaveAll.setText(_translate("MainWindow", "Save All..."))
        self.QSaveAll.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save All (Ctrl+Alt+S)</p></body></html>"))
        self.QSaveAll.setShortcut(_translate("MainWindow", "Ctrl+Alt+S"))
        # |_ Save Data Points
        self.QSaveDataPoints.setText(_translate("MainWindow", "Save Data Points..."))
        self.QSaveDataPoints.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save Data Points</p></body></html>"))
        # |_ Save Hit Points
        self.QSaveHitPoints.setText(_translate("MainWindow", "Save Hit Points..."))
        self.QSaveHitPoints.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save Hit Points</p></body></html>"))
        # |_ Save False Positives
        self.QSaveFalsePositives.setText(_translate("MainWindow", "Save False Positives..."))
        self.QSaveFalsePositives.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save False Positives</p></body></html>"))
        # |_ New
        self.QNew.setText(_translate("MainWindow", "New..."))
        self.QNew.setToolTip(_translate("MainWindow", "<html><head/><body><p>New (Ctrl+N)</p></body></html>"))
        self.QNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        # |_ Add
        self.QAdd.setText(_translate("MainWindow", "Add"))
        self.QAdd.setToolTip(_translate("MainWindow", "Add (Ctrl+A, Ctrl+Shift++)"))
        self.QAdd.setShortcut(_translate("MainWindow", "Ctrl+A, Ctrl+Shift++"))
        # |_ Delete
        self.QDelete.setText(_translate("MainWindow", "Delete"))
        self.QDelete.setToolTip(_translate("MainWindow", "Delete (Del, Ctrl+Shift+_)"))
        self.QDelete.setShortcut(_translate("MainWindow", "Del, Ctrl+Shift+_"))
        # |_ Edit
        self.QEdit.setText(_translate("MainWindow", "Edit"))
        self.QEdit.setToolTip(_translate("MainWindow", "Edit (Ctrl+E)"))
        self.QEdit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        # |_ Start
        self.QStart.setText(_translate("MainWindow", "Start"))
        self.QStart.setToolTip(_translate("MainWindow", "Start (P)"))
        self.QStart.setShortcut(_translate("MainWindow", "P"))

        self.Item = None

class QScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(QScene, self).__init__()

    def mousePressPos(self):
        return self.__mousePressPos

    def mousePressEvent(self, event):
        self.__mousePressPos = event.scenePos()
        super(QScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        try:
            super(QScene, self).setFocusItem(super(QScene, self).items(event.scenePos())[0])
        except:
            pass
        finally:
            super(QScene, self).mouseMoveEvent(event)