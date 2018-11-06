# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './displot.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.whatsNew = QtWidgets.QWidget()
        self.whatsNew.setObjectName("whatsNew")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.whatsNew)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.whatsNewBrowser = QtWidgets.QTextBrowser(self.whatsNew)
        self.whatsNewBrowser.setObjectName("whatsNewBrowser")
        self.gridLayout_2.addWidget(self.whatsNewBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.whatsNew, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionAbout.setObjectName("actionAbout")
        self.actionOpenImage = QtWidgets.QAction(MainWindow)
        self.actionOpenImage.setObjectName("actionOpenImage")
        self.actionOpen_Sequence = QtWidgets.QAction(MainWindow)
        self.actionOpen_Sequence.setObjectName("actionOpen_Sequence")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSaveImageAs = QtWidgets.QAction(MainWindow)
        self.actionSaveImageAs.setEnabled(False)
        self.actionSaveImageAs.setObjectName("actionSaveImageAs")
        self.actionQuick_scan = QtWidgets.QAction(MainWindow)
        self.actionQuick_scan.setEnabled(True)
        self.actionQuick_scan.setObjectName("actionQuick_scan")
        self.actionRemove_background = QtWidgets.QAction(MainWindow)
        self.actionRemove_background.setObjectName("actionRemove_background")
        self.actionCloseImage = QtWidgets.QAction(MainWindow)
        self.actionCloseImage.setEnabled(False)
        self.actionCloseImage.setObjectName("actionCloseImage")
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveImageAs)
        self.menuFile.addAction(self.actionCloseImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "displot"))
        self.whatsNewBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Roboto\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:600;\">Displot (alpha version)</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please submit feature requests and report any bugs to: <a href=\"https://github.com/bjstarosta/displot/issues\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/bjstarosta/displot/issues</span></a></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.whatsNew), _translate("MainWindow", "Welcome"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionOpenImage.setText(_translate("MainWindow", "Open Image"))
        self.actionOpen_Sequence.setText(_translate("MainWindow", "Open Sequence"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSaveImageAs.setText(_translate("MainWindow", "Save Image As..."))
        self.actionQuick_scan.setText(_translate("MainWindow", "Quick scan"))
        self.actionRemove_background.setText(_translate("MainWindow", "Remove background"))
        self.actionCloseImage.setText(_translate("MainWindow", "Close Image"))

