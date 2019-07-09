# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './displot.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.whatsNew = QtWidgets.QWidget()
        self.whatsNew.setObjectName("whatsNew")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.whatsNew)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.whatsNewBrowser = QtWidgets.QTextBrowser(self.whatsNew)
        self.whatsNewBrowser.setOpenExternalLinks(True)
        self.whatsNewBrowser.setOpenLinks(True)
        self.whatsNewBrowser.setObjectName("whatsNewBrowser")
        self.gridLayout_3.addWidget(self.whatsNewBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.whatsNew, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.consoleFrame = Console(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consoleFrame.sizePolicy().hasHeightForWidth())
        self.consoleFrame.setSizePolicy(sizePolicy)
        self.consoleFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.consoleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.consoleFrame.setObjectName("consoleFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.consoleFrame)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.consoleTitle = QtWidgets.QWidget(self.consoleFrame)
        self.consoleTitle.setMinimumSize(QtCore.QSize(0, 16))
        self.consoleTitle.setMaximumSize(QtCore.QSize(16777215, 16))
        self.consoleTitle.setObjectName("consoleTitle")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.consoleTitle)
        self.horizontalLayout.setContentsMargins(9, 1, 9, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.consoleTitleLabel = QtWidgets.QPushButton(self.consoleTitle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consoleTitleLabel.sizePolicy().hasHeightForWidth())
        self.consoleTitleLabel.setSizePolicy(sizePolicy)
        self.consoleTitleLabel.setObjectName("consoleTitleLabel")
        self.horizontalLayout.addWidget(self.consoleTitleLabel)
        self.consoleTitleHLine = QtWidgets.QFrame(self.consoleTitle)
        self.consoleTitleHLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.consoleTitleHLine.setMidLineWidth(0)
        self.consoleTitleHLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.consoleTitleHLine.setObjectName("consoleTitleHLine")
        self.horizontalLayout.addWidget(self.consoleTitleHLine)
        self.verticalLayout_3.addWidget(self.consoleTitle)
        self.consoleTextBox = QtWidgets.QTextEdit(self.consoleFrame)
        self.consoleTextBox.setEnabled(True)
        self.consoleTextBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.consoleTextBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.consoleTextBox.setLineWidth(1)
        self.consoleTextBox.setMidLineWidth(0)
        self.consoleTextBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.consoleTextBox.setUndoRedoEnabled(False)
        self.consoleTextBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.consoleTextBox.setObjectName("consoleTextBox")
        self.verticalLayout_3.addWidget(self.consoleTextBox)
        self.verticalLayout.addWidget(self.consoleFrame)
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
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
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
        self.actionSaveImageAs.setEnabled(True)
        self.actionSaveImageAs.setObjectName("actionSaveImageAs")
        self.actionQuick_scan = QtWidgets.QAction(MainWindow)
        self.actionQuick_scan.setEnabled(True)
        self.actionQuick_scan.setObjectName("actionQuick_scan")
        self.actionRemove_background = QtWidgets.QAction(MainWindow)
        self.actionRemove_background.setObjectName("actionRemove_background")
        self.actionCloseImage = QtWidgets.QAction(MainWindow)
        self.actionCloseImage.setEnabled(True)
        self.actionCloseImage.setObjectName("actionCloseImage")
        self.actionExcludeArea = QtWidgets.QAction(MainWindow)
        self.actionExcludeArea.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/scissors.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExcludeArea.setIcon(icon)
        self.actionExcludeArea.setObjectName("actionExcludeArea")
        self.actionSelectObject = QtWidgets.QAction(MainWindow)
        self.actionSelectObject.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/navigation-2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelectObject.setIcon(icon1)
        self.actionSelectObject.setObjectName("actionSelectObject")
        self.actionHideAllObjects = QtWidgets.QAction(MainWindow)
        self.actionHideAllObjects.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/eye.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/eye-off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionHideAllObjects.setIcon(icon2)
        self.actionHideAllObjects.setObjectName("actionHideAllObjects")
        self.actionRemoveExclusion = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/trash.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemoveExclusion.setIcon(icon3)
        self.actionRemoveExclusion.setObjectName("actionRemoveExclusion")
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveImageAs)
        self.menuFile.addAction(self.actionCloseImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionSelectObject)
        self.toolBar.addAction(self.actionHideAllObjects)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExcludeArea)
        self.toolBar.addAction(self.actionRemoveExclusion)

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
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600;\">Displot</span><span style=\" font-weight:296;\"> </span><span style=\" font-size:14pt; font-weight:296;\">- </span><span style=\" font-size:14pt;\">GaN Dislocation Counter</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:12pt;\">Repository address: </span><a href=\"https://github.com/bjstarosta/displot\"><span style=\" font-family:\'Noto Sans\'; font-size:12pt; text-decoration: underline; color:#0000ff;\">https://github.com/bjstarosta/displot</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Noto Sans\'; font-size:9pt;\">Use the &quot;File&quot; menu to load images into the program. Only 8-bit greyscale TIF images are supported, support for more may be added based on need. The dislocation detection method is currently crude, but should improve in further releases as we put together datasets for training a machine learning algorithm. For now, expect to have to heavily help it along by marking dislocations that have been missed and unmarking false positives - the UI is designed to be as helpful with regards to that as possible. If you want to discuss anything about this program further, email me at </span><a href=\"mailto:bohdan.starosta@strath.ac.uk\"><span style=\" font-family:\'Noto Sans\'; font-size:9pt; text-decoration: underline; color:#0000ff;\">bohdan.starosta@strath.ac.uk</span></a><span style=\" font-family:\'Noto Sans\'; font-size:9pt;\"> or use the GitHub issue tracker.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is a first release version, there may be bugs. If a new version is released, expect a dialog nagging you to upgrade.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Please submit feature requests and report any bugs to: </span><a href=\"https://github.com/bjstarosta/displot/issues\"><span style=\" font-weight:600; text-decoration: underline; color:#0000ff;\">https://github.com/bjstarosta/displot/issues</span></a></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.whatsNew), _translate("MainWindow", "Welcome"))
        self.consoleTitleLabel.setText(_translate("MainWindow", "Console"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionOpenImage.setText(_translate("MainWindow", "Open Image"))
        self.actionOpen_Sequence.setText(_translate("MainWindow", "Open Sequence"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSaveImageAs.setText(_translate("MainWindow", "Save Image As..."))
        self.actionQuick_scan.setText(_translate("MainWindow", "Quick scan"))
        self.actionRemove_background.setText(_translate("MainWindow", "Remove background"))
        self.actionCloseImage.setText(_translate("MainWindow", "Close Image"))
        self.actionExcludeArea.setText(_translate("MainWindow", "Exclude Area"))
        self.actionExcludeArea.setToolTip(_translate("MainWindow", "Select an area on the image to exclude all search results from."))
        self.actionSelectObject.setText(_translate("MainWindow", "Select Object"))
        self.actionSelectObject.setToolTip(_translate("MainWindow", "Object selection tool."))
        self.actionHideAllObjects.setText(_translate("MainWindow", "Hide All Objects"))
        self.actionHideAllObjects.setToolTip(_translate("MainWindow", "Toggle hiding all feature objects."))
        self.actionRemoveExclusion.setText(_translate("MainWindow", "Remove Exclusion"))
        self.actionRemoveExclusion.setToolTip(_translate("MainWindow", "Click this while an exclusion area is selected to remove it."))
from displot.ui_widgets import Console
from . import feathericons_rc