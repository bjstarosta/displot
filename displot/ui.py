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
        self.updateWindowTitle()

    def run(self):
        """Run this method to show the GUI, then block until window is closed.

        All non-event code running after this method will not execute!
        """
        self.window.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Exits the program."""
        self.app.quit()

    def setStatusBar(self, message=""):
        self.window.statusBar().showMessage(message)

    def updateWindowTitle(self):
        title = self.appTitle + ' v.' + self.appVersion + ' - ['
        it = self.imageTabFind(self.tabWidget.currentIndex())

        if it == False:
            curFile = 'No image'
        else:
            curFile = it.filePath

        title = title + curFile + ']'
        self.window.setWindowTitle(title)

    def imageFileDlgOpen(self):
        dlg = QtWidgets.QFileDialog(self.window, 'Open image')
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        #dlg.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
        dlg.setNameFilters(['Image files (*.tif)', 'All files (*)'])

        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            return dlg.selectedFiles()[0]
        else:
            return False

    def imageTabOpen(self, imageHandle, tabName="No image"):
        it = ImageTab(self.tabWidget, self.imageTabUi)
        it.open(imageHandle, tabName)
        self.imageTabs.append(it)

    def imageTabClose(self, index):
        it = self.imageTabFind(index)
        if not isinstance(it, ImageTab):
            return
        it.close()
        self.imageTabs.remove(it)

    def imageTabFind(self, index):
        """Finds the ImageTab object corresponding with the tab at specified index.

        Returns either an ImageTab object or False if no corresponding object
        was found.
        """
        if index == -1:
            return False

        for o in self.imageTabs:
            if o.widgetIndex == index:
                return o
        return False


class ImageTab(QtWidgets.QWidget):
    """Tab widget container.

    Attributes:
        opened: Returns True if the open() method was called, False otherwise.
        imageHandle: An Image() object reference (see imageutils.py).
        widgetIndex: Current index of the tab in the tabWidget object.
            Note that the index isn't static and can change based on tabs
            being dragged around.
    """

    def __init__(self, tabWidgetRef, layoutRef):
        QtWidgets.QWidget.__init__(self)
        layoutRef.setupUi(self)

        self.opened = False
        self.imageHandle = False

        self._imageScene = QtWidgets.QGraphicsScene()
        self._imageView = self.findChild(QtWidgets.QGraphicsView, "imageView")
        self._imageView.setScene(self._imageScene)
        self._minimapView = self.findChild(QtWidgets.QGraphicsView, "minimap")
        self._minimapView.setScene(self._imageScene)
        self._qPixMap = False
        self._qImage = False

        self._tabWidget = tabWidgetRef

    def open(self, imageHandle, tabName):
        if self.opened == True:
            return
        self._tabWidget.addTab(self, tabName)
        self._tabWidget.setCurrentIndex(self.widgetIndex)

        self.imageHandle = imageHandle

        self._qImage = self._grayscale2QImage(self.imageHandle.data)
        self.redrawImage()

        self.opened = True

    def close(self):
        if self.opened == False:
            return
        self._tabWidget.removeTab(self.widgetIndex)

    def redrawImage(self):
        self._qPixMap = QtGui.QPixmap.fromImage(self._qImage)
        self._imageScene.addPixmap(self._qPixMap)

        #self._minimapView.fitInView(QtCore.QRectF())
        #rect1 = self._minimapView.viewport().rect()
        #print(rect1)
        #rect = self._minimapView.mapToScene(self._minimapView.viewport().rect()).boundingRect();
        #print(rect)
        #self._minimapView.fitInView(rect)

        rect = self._minimapView.rect()
        h, w = self.imageHandle.data.shape
        w_ratio = self._minimapView.rect().width() / w
        h_ratio = self._minimapView.rect().height() / h
        if w_ratio > h_ratio:
            ratio = h_ratio
        else:
            ratio = w_ratio
        ratio = ratio * 0.95
        self._minimapView.scale(ratio, ratio)

        self._minimapView.show()
        self._imageView.show()

    def setTabLabel(self, label):
        self._tabWidget.setTabText(self.widgetIndex, label)

    @property
    def filePath(self):
        return self.imageHandle.filePath

    @property
    def widgetIndex(self):
        return self._tabWidget.indexOf(self)

    def _grayscale2QImage(self, imageData):
        h, w = imageData.shape
        result = QtGui.QImage(w, h, QtGui.QImage.Format_Indexed8)

        for i in range(256):
            result.setColor(i, QtGui.qRgb(i,i,i))

        y = 0
        for xRow in imageData:
            x = 0
            for color in xRow:
                result.setPixel(x, y, color)
                x += 1
            y += 1

        return result
