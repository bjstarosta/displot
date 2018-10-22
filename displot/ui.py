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
        self.info = infoDict
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
        """Shows a short message in the status bar at the bottom of the window."""
        self.window.statusBar().showMessage(message)

    def updateWindowTitle(self):
        """Updates the windowbar title to reflect the currently focused image file."""
        title = self.appTitle + ' v.' + self.appVersion + ' - ['
        it = self.imageTabFind(self.tabWidget.currentIndex())

        if it == False:
            curFile = 'No image'
        else:
            curFile = it.filePath

        title = title + curFile + ']'
        self.window.setWindowTitle(title)

    def imageFileDlgOpen(self):
        """Opens a file browser dialog used for selecting an image file to be
        opened. Returns either a file path string or False if the dialog was
        cancelled.
        """
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
        """Creates and focuses a new tab in the tab widget using the specified
        image file.

        Attributes:
            imageHandle: An Image() object reference (see imageutils.py).
            tabName: A text string to be shown as the tab label.
        """
        it = ImageTab(self.tabWidget, self.imageTabUi)
        it.open(imageHandle, tabName)
        self.imageTabs.append(it)

    def imageTabClose(self, index):
        """Closes the tab specified by the index argument.

        Attributes:
            index: An integer specifying the index of the tab to close from
                the left-hand side.
        """
        it = self.imageTabFind(index)
        if not isinstance(it, QtWidgets.QWidget):
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

    def openAbout(self):
        dlg = QtWidgets.QDialog()
        self.aboutUi.setupUi(dlg)

        browser = dlg.findChild(QtWidgets.QTextBrowser, "textBrowser")
        html = str(browser.toHtml())
        html = html.replace('{version}', self.appVersion)
        html = html.replace('{author}', self.info['author'])
        html = html.replace('{author_email}', self.info['authorEmail'])
        html = html.replace('{project_page}', self.info['projectPage'])
        browser.setHtml(html)

        dlg.show()
        dlg.exec_()


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

        self._qImage = False
        self._qPixMap = False
        self._imageScenePixmap = False
        self._minimapScenePixmap = False
        self._tabWidget = tabWidgetRef

        # Init main image view layout objects
        self._imageScene = QtWidgets.QGraphicsScene()
        self._imageView = self.findChild(QtWidgets.QGraphicsView, "imageView")
        self._imageView.setScene(self._imageScene)
        self._imageView.imageTab = self
        self._imageView.initEvents()

        # Init minimap layout objects
        self._minimapScene = QtWidgets.QGraphicsScene()
        self._minimapView = self.findChild(QtWidgets.QGraphicsView, "minimap")
        self._minimapView.setScene(self._minimapScene)
        self._minimapView.imageTab = self

    def open(self, imageHandle, tabName):
        """Sets up the UI for the image referenced in imageHandle."""
        if self.opened == True:
            return
        self._tabWidget.addTab(self, tabName)
        self._tabWidget.setCurrentIndex(self.widgetIndex)

        self.imageHandle = imageHandle
        self.redrawImage()
        self._minimapView.show()
        self._imageView.show()

        self._minimapView.drawViewbox()

        # Populate the infobox
        ibText = '"' + imageHandle.filePath + '"'
        ibText += ' [W:' + str(imageHandle.imageDim[0])
        ibText += ', H:' + str(imageHandle.imageDim[1]) + ']'
        ibText += ' [' + imageHandle.fileSize + ']'
        infoBox = self.findChild(QtWidgets.QLabel, "imageInfoLabel")
        infoBox.setText(ibText)

        self.opened = True

    def close(self):
        """Destroys the tab and cleans up."""
        if self.opened == False:
            return
        self._tabWidget.removeTab(self.widgetIndex)

    def redrawImage(self):
        """If there have been changes to the self.imageHandle object reference,
        call this function to apply them to the viewports.
        """
        self._qImage = self._grayscale2QImage(self.imageHandle.data)
        self._qPixMap = QtGui.QPixmap.fromImage(self._qImage)
        if isinstance(self._imageScenePixmap, bool):
            self._imageScenePixmap = self._imageScene.addPixmap(self._qPixMap)
            self._minimapScenePixmap = self._minimapScene.addPixmap(self._qPixMap)
        else:
            self._imageScenePixmap.setPixmap(self._qPixMap)
            self._minimapScenePixmap.setPixmap(self._qPixMap)

        #self._minimapView.fitInView(self._imageScene.itemsBoundingRect(),
        #    QtCore.Qt.KeepAspectRatio)
        ratio = self._minimapView.getMinimapRatio()
        self._minimapScenePixmap.setScale(ratio)

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

        # Load data directly from the numpy array into QImage
        result = QtGui.QImage(imageData.data, w, h, QtGui.QImage.Format_Indexed8)
        result.ndarray = imageData

        # Set up the monochrome colour palette
        for i in range(256):
            result.setColor(i, QtGui.qRgb(i,i,i))

        return result
