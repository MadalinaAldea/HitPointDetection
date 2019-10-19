# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExitWithoutSave.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class UiExitWithoutSave(object):
    def setupUi(self, ExitWithoutSave):
        ExitWithoutSave.setObjectName("ExitWithoutSave")
        ExitWithoutSave.resize(217, 73)
        self.gridLayout = QtWidgets.QGridLayout(ExitWithoutSave)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_save = QtWidgets.QPushButton(ExitWithoutSave)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_dontSave = QtWidgets.QPushButton(ExitWithoutSave)
        self.pushButton_dontSave.setObjectName("pushButton_dontSave")
        self.horizontalLayout.addWidget(self.pushButton_dontSave)
        self.pushButton_cancel = QtWidgets.QPushButton(ExitWithoutSave)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(ExitWithoutSave)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/Question/resources/icons8-help-32.png"))
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(ExitWithoutSave)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(ExitWithoutSave)
        self.pushButton_cancel.clicked['bool'].connect(ExitWithoutSave.close)
        QtCore.QMetaObject.connectSlotsByName(ExitWithoutSave)

    def retranslateUi(self, ExitWithoutSave):
        _translate = QtCore.QCoreApplication.translate
        ExitWithoutSave.setWindowTitle(_translate("ExitWithoutSave", "Form"))
        self.pushButton_save.setText(_translate("ExitWithoutSave", "Save"))
        self.pushButton_dontSave.setText(_translate("ExitWithoutSave", "Don\'t save"))
        self.pushButton_cancel.setText(_translate("ExitWithoutSave", "Cancel"))
        self.label_2.setText(_translate("ExitWithoutSave", "Do you want to save your changes before exit?"))
import dialog.rsc
