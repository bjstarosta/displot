# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from ui_def import *

class DisplotUi(object):
    """Singleton object responsible for UI operations.

    Attributes:
        app: Qt QApplication object
        window: Qt QMainWindow object
        appTitle: String defining the window title
    """

    def __init__(self, infoDict):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()

        # Load UI defs here
        self._windowUi = ui_displot.Ui_MainWindow()
        self._windowUi.setupUi(self.window)
        self._aboutUi = ui_displot_about.Ui_AboutDialog()
        self._imageTabUi = ui_displot_image.Ui_ImageTabPrototype()

        # Reference important UI objects
        self.windowTabs = self._windowUi.tabWidget
        self.imageTabs = []

        # Setup common events
        self.windowTabs.tabBarClicked.connect(self._evTabBarClicked)

        self._windowUi.actionOpenImage.triggered.connect(self.imageTabOpen)
        self._windowUi.actionExit.triggered.connect(self.exit)

        self.appTitle = infoDict['appTitle']
        self.appVersion = infoDict['appVersion']
        self.setWindowTitle()

    def run(self):
        """Run this method to show the GUI, then block until window is closed.

        All non-event code running after this method will not execute!
        """
        self.window.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Exits the program."""
        self.app.quit()

    def setWindowTitle(self, curFile=False):
        title = self.appTitle + ' v.' + self.appVersion + ' - ['
        if curFile == False:
            curFile = 'No image'
        title = title + curFile + ']'
        self.window.setWindowTitle(title)

    def setStatusBar(self, message):
        self.window.statusBar().showMessage(message)

    def imageTabOpen(self):
        imageTab = QtWidgets.QWidget()
        self._imageTabUi.setupUi(imageTab)
        self.windowTabs.addTab(imageTab, "No Image")
        self.setStatusBar(str(self.windowTabs.currentIndex()) + ' ' + str(self.windowTabs.indexOf(imageTab)))
        self.windowTabs.setCurrentIndex(self.windowTabs.indexOf(imageTab))
        #self.windowTabs.setTabText(self.windowTabs.indexOf(imageTab), "No Image")

    def imageTabClose(self):
        #self.windowTabs.removeTab(self.windowTabs.indexOf(self._windowUi.imageTab))
        pass

    def _evTabBarClicked(self, index):
        if index == 0:
            self.imageTabOpen()
        else:
            pass
