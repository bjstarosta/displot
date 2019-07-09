# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './displot_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogBox(object):
    def setupUi(self, DialogBox):
        DialogBox.setObjectName("DialogBox")
        DialogBox.resize(320, 140)
        DialogBox.setMaximumSize(QtCore.QSize(320, 140))
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogBox)
        self.buttonBox.setGeometry(QtCore.QRect(10, 100, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dialogText = QtWidgets.QLabel(DialogBox)
        self.dialogText.setGeometry(QtCore.QRect(10, 10, 301, 81))
        self.dialogText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.dialogText.setWordWrap(True)
        self.dialogText.setObjectName("dialogText")

        self.retranslateUi(DialogBox)
        self.buttonBox.accepted.connect(DialogBox.accept)
        self.buttonBox.rejected.connect(DialogBox.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogBox)

    def retranslateUi(self, DialogBox):
        _translate = QtCore.QCoreApplication.translate
        DialogBox.setWindowTitle(_translate("DialogBox", "Dialog"))
        self.dialogText.setText(_translate("DialogBox", "TextLabel"))
