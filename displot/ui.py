# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from uiDefs import *

class DisplotUi(object):
    """Singleton object responsible for UI operations.

    Attributes:
        app: Qt QApplication object
        window: Qt QMainWindow object
        appTitle: String defining the window title
    """

    def __init__(self, infoDict={}):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()

        self.imageTabs = []

        # Load UI defs here
        self.windowUi = ui_displot.Ui_MainWindow()
        self.windowUi.setupUi(self.window)
        self.aboutUi = ui_displot_about.Ui_AboutDialog()
        self.imageTabUi = ui_displot_image.Ui_ImageTabPrototype()

        # Reference important UI objects
        self.tabWidget = self.windowUi.tabWidget

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

    def setStatusBar(self, message=""):
        self.window.statusBar().showMessage(message)

    def imageTabOpen(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.window, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)

        imageTab = ImageTab(self.tabWidget, self.imageTabUi)
        imageTab.open()
        self.imageTabs.append(imageTab)

    def imageTabClose(self, index):
        imageTab = self.imageTabFind(index)
        if isinstance(imageTab, ImageTab):
            imageTab.close()

    def imageTabFind(self, index):
        """Finds the ImageTab object corresponding with the tab at specified index.

        Returns either an ImageTab object or False if no corresponding object
        was found.
        """
        for o in self.imageTabs:
            if o.widgetIndex == index:
                return o
        return False


class ImageTab(QtWidgets.QWidget):
    """Tab widget container.

    Attributes:
        opened: Returns True if the open() method was called, False otherwise.
        widgetIndex: Current index of the tab in the tabWidget object.
            Note that the index isn't static and can change based on tabs
            being dragged around.
    """

    def __init__(self, tabWidgetRef, layoutRef):
        QtWidgets.QWidget.__init__(self)

        self.opened = False
        self._tabWidget = tabWidgetRef

        layoutRef.setupUi(self)

    def open(self, imageHandle, tabName="No image"):
        if self.opened == True:
            return
        self._tabWidget.addTab(self, tabName)
        self._tabWidget.setCurrentIndex(self.widgetIndex)
        self.opened = True

    def close(self):
        if self.opened == False:
            return
        self._tabWidget.removeTab(self.widgetIndex)

    def setTabLabel(self, label, opts):
        self._tabWidget.setTabText(self.widgetIndex, label)

    @property
    def widgetIndex(self):
        return self._tabWidget.indexOf(self)
