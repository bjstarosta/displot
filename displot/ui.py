# -*- coding: utf-8 -*-
import os, sys, gc
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from uiDefs import *

import imageutils


class DisplotUi(QtWidgets.QMainWindow):
    """Singleton object responsible for UI operations.

    Attributes:
        app: Qt QApplication object
        window: Qt QMainWindow object
        appTitle: String defining the window title
    """

    def __init__(self, infoDict={}):
        self.app = QtWidgets.QApplication(sys.argv)

        super().__init__()

        self.layout = ui_displot.Ui_MainWindow()
        self.layout.setupUi(self)

        self.imageTabs = []

        # Reference important UI objects
        self.tabWidget = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.appTitle = infoDict['appTitle']
        self.appVersion = infoDict['appVersion']
        self.info = infoDict
        self.updateWindowTitle()

        # Setup events
        self.tabWidget.tabCloseRequested.connect(self.imageTabClose)
        self.tabWidget.currentChanged.connect(self.updateWindowTitle)
        self.tabWidget.currentChanged.connect(self.refreshMenus)

        self.layout.actionOpenImage.triggered.connect(self.imageTabOpen)
        self.layout.actionCloseImage.triggered.connect(self.imageTabClose)
        self.layout.actionExit.triggered.connect(self.exit)

        self.layout.actionAbout.triggered.connect(self.openAbout)

    def run(self):
        """Run this method to show the GUI, then block until window is closed.

        All non-event code running after this method will not execute!
        """
        self.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Exits the program."""
        gc.collect(1)
        self.app.quit()

    def closeEvent(self, ev):
        self.exit()

    def setStatusBarMsg(self, message=""):
        """Shows a short message in the status bar at the bottom of the window."""
        self.statusBar().showMessage(message)

    def refreshMenus(self):
        if self.tabWidget.currentIndex() == -1:
            enable = False
        else:
            enable = True

        imageMenus = [
            self.layout.actionSaveImageAs,
            self.layout.actionCloseImage
        ]
        for m in imageMenus:
            m.setEnabled(enable)

    def updateWindowTitle(self):
        """Updates the windowbar title to reflect the currently focused image file."""
        title = self.appTitle + ' v.' + self.appVersion + ' - ['
        it = self.imageTabFind(self.tabWidget.currentIndex())

        if it == False:
            curFile = 'No image'
        else:
            curFile = it.filePath

        title = title + curFile + ']'
        self.setWindowTitle(title)

    def imageTabOpen(self):
        """Wrapper method for a few methods in this class. Will launch a file
        browser dialog to get a file path, then load that file path into a new
        tab.
        """
        filePath = self.imageFileDlgOpen()
        if filePath == False:
            return

        image = imageutils.Image(filePath)

        self.setStatusBarMsg('Loading image file: ' + filePath)
        self.imageTabCreate(image, os.path.basename(filePath))
        self.updateWindowTitle()
        self.setStatusBarMsg('Done.')

    def imageFileDlgOpen(self):
        """Opens a file browser dialog used for selecting an image file to be
        opened. Returns either a file path string or False if the dialog was
        cancelled.
        """
        dlg = QtWidgets.QFileDialog(self, 'Open image')
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        #dlg.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
        dlg.setNameFilters(['Image files (*.tif)', 'All files (*)'])

        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            return dlg.selectedFiles()[0]
        else:
            return False

    def imageTabCreate(self, imageHandle, tabName="No image"):
        """Creates and focuses a new tab in the tab widget using the specified
        image file.

        Attributes:
            imageHandle: An Image() object reference (see imageutils.py).
            tabName: A text string to be shown as the tab label.
        """
        it = ImageTab(self, self.tabWidget)
        it.open(imageHandle, tabName)
        self.imageTabs.append(it)
        return it

    def imageTabClose(self, index=False):
        """Closes the tab specified by the index argument.

        Attributes:
            index: An integer specifying the index of the tab to close from
                the left-hand side.
        """
        if index == False:
            it = self.imageTabCurrent()
        else:
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

    def imageTabCurrent(self):
        return self.imageTabFind(self.tabWidget.currentIndex())

    def openAbout(self):
        dlg = AboutDialog(self.info)
        dlg.show()
        dlg.exec_()


class AboutDialog(QtWidgets.QDialog):
    """About window object.
    """

    def __init__(self, infoDict={}):
        super().__init__()

        self.layout = ui_displot_about.Ui_AboutDialog()
        self.layout.setupUi(self)

        browser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")
        html = str(browser.toHtml())
        html = html.replace('{version}', infoDict['appVersion'])
        html = html.replace('{author}', infoDict['author'])
        html = html.replace('{author_email}', infoDict['authorEmail'])
        html = html.replace('{project_page}', infoDict['projectPage'])
        browser.setHtml(html)


class GenericDialog(QtWidgets.QDialog):
    """Generic dialog window object.
    """

    def __init__(self):
        super().__init__()

        self.layout = ui_displot_dialog.Ui_DialogBox()
        self.layout.setupUi(self)

    def setText(self, text):
        label = self.findChild(QtWidgets.QLabel, "dialogText")
        label.setText(text)

    def setAccept(self, func):
        btn = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        return btn.accepted.connect(func)

    def setReject(self):
        btn = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        return btn.rejected.connect(func)


class ImageTab(QtWidgets.QWidget):
    """Tab widget container.

    Attributes:
        opened: Returns True if the open() method was called, False otherwise.
        imageHandle: An Image() object reference (see imageutils.py).
        widgetIndex: Current index of the tab in the tabWidget object.
            Note that the index isn't static and can change based on tabs
            being dragged around.
    """

    def __init__(self, windowRef, tabWidgetRef):
        super().__init__()

        self.layout = ui_displot_image.Ui_ImageTabPrototype()
        self.layout.setupUi(self)

        self.opened = False
        self.imageHandle = False
        self.imageFragments = []

        self._qImage = False
        self._qPixMap = False
        self._imageScenePixmap = False
        self._minimapScenePixmap = False
        self._window = windowRef
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

        # Init button events
        self._imageScanBtn = self.findChild(QtWidgets.QPushButton, "button_Scan")
        self._imageScanBtn.clicked.connect(self.scanImage)

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
        ibText += ' [W:' + str(imageHandle.dimensions['w'])
        ibText += ', H:' + str(imageHandle.dimensions['h']) + ']'
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

    def scanImage(self):
        """Begins the process of scanning the image for dislocations.
        Will apply movable region objects to the main graphics view on completion.
        """
        self._imageScanBtn.setEnabled(False)
        self._window.setStatusBarMsg(
            'Scanning for dislocations... (edge detection)')

        edgeData = imageutils.edgeDetection(
            image=self.imageHandle.data,
            sigma=self.findChild(
                QtWidgets.QDoubleSpinBox,
                "value_GaussianSigma"
            ).cleanText(),
            min_area=self.findChild(
                QtWidgets.QSpinBox,
                "value_DiscardLabels"
            ).cleanText(),
            margin=self.findChild(
                QtWidgets.QSpinBox,
                "value_DiscardMargins"
            ).cleanText(),
            region_class=ImageTabRegion
        )

        self._window.setStatusBarMsg(
            'Scanning for dislocations... (GLCM)')

        # Generate angle list
        angles_num = int(self.findChild(
            QtWidgets.QSpinBox,
            "value_AnglesCompared"
        ).cleanText())
        angles = [0]
        angles_i = 1
        while angles_i < angles_num:
            angles.append((angles_i * np.pi) / angles_num)
            angles_i += 1

        glcmData = imageutils.testGLCM(
            image=self.imageHandle.data,
            region_list=edgeData[0],
            angles=angles,
            patch_size=self.findChild(
                QtWidgets.QSpinBox,
                "value_PatchSize"
            ).cleanText(),
            targets=(
                self.findChild(
                    QtWidgets.QDoubleSpinBox,
                    "value_DissimilarityTarget"
                ).cleanText(),
                self.findChild(
                    QtWidgets.QDoubleSpinBox,
                    "value_CorrelationTarget"
                ).cleanText()
            ),
            tolerances=(
                self.findChild(
                    QtWidgets.QDoubleSpinBox,
                    "value_DissimilarityTolerance"
                ).cleanText(),
                self.findChild(
                    QtWidgets.QDoubleSpinBox,
                    "value_CorrelationTolerance"
                ).cleanText()
            )
        )

        self._window.setStatusBarMsg(
            'Done. {} dislocation candidates found.'.format(len(glcmData[0])))
        self._imageScanBtn.setEnabled(True)

    def setTabLabel(self, label):
        """Sets the tab label to the specified text.

        Attributes:
            label: A text string to be inserted into the tab label.
        """
        self._tabWidget.setTabText(self.widgetIndex, label)

    @property
    def filePath(self):
        return self.imageHandle.filePath

    @property
    def widgetIndex(self):
        return self._tabWidget.indexOf(self)

    def _grayscale2QImage(self, imageData):
        """Converts data from a grayscale numpy array into a QImage object for
        manipulation by Qt.

        Attributes:
            imageData: numpy ndarray of the image.
        """
        h, w = imageData.shape

        # Load data directly from the numpy array into QImage
        result = QtGui.QImage(imageData.data, w, h, QtGui.QImage.Format_Indexed8)
        result.ndarray = imageData

        # Set up the monochrome colour palette
        for i in range(256):
            result.setColor(i, QtGui.qRgb(i,i,i))

        return result


class ImageTabRegion(imageutils.ImageRegion):
    def show(self, imageTab):
        pass

    def hide(self, imageTab):
        pass

    def highlight(self, imageTab):
        pass

    def centerOn(self, imageTab):
        pass
