# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './displot.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
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
        self.centralWidgetLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.centralWidgetLayout.setContentsMargins(2, 2, 2, 4)
        self.centralWidgetLayout.setObjectName("centralWidgetLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.centralWidgetLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuScan = QtWidgets.QMenu(self.menubar)
        self.menuScan.setEnabled(False)
        self.menuScan.setObjectName("menuScan")
        self.menuImage = QtWidgets.QMenu(self.menubar)
        self.menuImage.setEnabled(False)
        self.menuImage.setObjectName("menuImage")
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
        self.menuScan.addAction(self.actionQuick_scan)
        self.menuImage.addAction(self.actionRemove_background)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuScan.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "displot"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuScan.setTitle(_translate("MainWindow", "Scan"))
        self.menuImage.setTitle(_translate("MainWindow", "Image"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionOpenImage.setText(_translate("MainWindow", "Open Image"))
        self.actionOpen_Sequence.setText(_translate("MainWindow", "Open Sequence"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSaveImageAs.setText(_translate("MainWindow", "Save Image As..."))
        self.actionQuick_scan.setText(_translate("MainWindow", "Quick scan"))
        self.actionRemove_background.setText(_translate("MainWindow", "Remove background"))
        self.actionCloseImage.setText(_translate("MainWindow", "Close Image"))

