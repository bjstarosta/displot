# -*- coding: utf-8 -*-
import os
import sys
import gc
import numpy as np

from PyQt5 import QtGui, QtWidgets
from uiDefs import ui_displot, ui_displot_about, ui_displot_dialog, ui_displot_image

import imageutils
from ui_widgets import WorkImageView


class DisplotUi(QtWidgets.QMainWindow):
    """Singleton object responsible for UI operations.

    This object, once instantiated, holds all the program data and definitions
    in a hierarchy of objects.

    Attributes:
        app (:obj:`QApplication`): Qt application object
        layout (:obj:`Ui_MainWindow`): Object holding all the layout definitions
            for the QMainWindow generated from the .ui files in the /devel/ directory.
        imageTabs (list): List of ImageTab objects holding the currently opened
            images.
        tabWidget (:obj:`QTabWidget`): Reference to the QTabWidget holding the
            opened images.
        appTitle (str): Application title as shown at the top of the window.
        appVersion (str): Application version as shown at the top of the window.
        info (dict): A dictionary holding program metadata.

    """

    IMAGE_SAVE_FILTERS = {
        'image/png': ['Portable network graphics image (*.png)', 'png'],
        'text/csv': ['Comma separated value file (*.csv)', 'csv']
    }

    def __init__(self, infoDict={}):
        """Class constructor.

        Connects up events and sets up the layout for the run() method.

        Args:
            infoDict (dict): Optional program metadata.

        """

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
        self.tabWidget.tabCloseRequested.connect(self.imageTabCloseDialog)
        self.tabWidget.currentChanged.connect(self.updateWindowTitle)
        self.tabWidget.currentChanged.connect(self.refreshMenus)

        self.layout.actionOpenImage.triggered.connect(self.imageTabOpen)
        self.layout.actionSaveImageAs.triggered.connect(self.imageTabSave)
        self.layout.actionCloseImage.triggered.connect(self.imageTabCloseDialog)
        self.layout.actionExit.triggered.connect(self.exit)
        self.layout.actionSaveImageAs.setEnabled(False)
        self.layout.actionCloseImage.setEnabled(False)

        self.layout.actionAbout.triggered.connect(self.openAbout)

    def run(self):
        """Run this method to show the GUI, then block until window is closed.

        All non-event code running after this method will not execute!
        """
        self.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Exits the program gracefully.
        """

        gc.collect(1)
        self.app.quit()

    def closeEvent(self, ev):
        """Event handler reimplementation for the window close event.

        Wrapper function.
        """

        self.exit()

    def setStatusBarMsg(self, message="", timeout=0):
        """Shows a short message in the status bar at the bottom of the window.
        """

        """Shows a short message in the status bar at the bottom of the window.

        Args:
            message (str): The message to show in the status bar.
            timeout (int): Amount of time in seconds after which the message
                will disappear. By default it's set to 0, which means the
                message will stay shown until replaced with something else.

        """

        self.statusBar().showMessage(message, timeout)

    def refreshMenus(self):
        """Makes sure menu item actions will effect the correct tab.
        """

        if isinstance(self.tabWidget.currentWidget(), ImageTab):
            enable = True
        else:
            enable = False

        imageMenus = [
            self.layout.actionSaveImageAs,
            self.layout.actionCloseImage
        ]
        for m in imageMenus:
            m.setEnabled(enable)

    def updateWindowTitle(self):
        """Updates the windowbar title to reflect the currently focused image file.
        """

        title = self.appTitle + ' v.' + self.appVersion + ' - ['
        it = self.imageTabFind(self.tabWidget.currentIndex())

        if it == None:
            curFile = 'No image'
        else:
            curFile = it.filePath

        title = title + curFile + ']'
        self.setWindowTitle(title)

    def imageTabOpen(self):
        """Wrapper method for the process of opening a new tab.

        Will launch a file browser dialog to get a file path, then load that
        file path into a new tab.
        """

        filePath = self.imageFileDlgOpen()
        if filePath == False:
            return

        image = imageutils.Image(filePath)

        self.setStatusBarMsg('Loading image file: ' + filePath)
        self.imageTabCreate(image, os.path.basename(filePath))
        self.updateWindowTitle()
        self.setStatusBarMsg('Done.', 3)

    def imageFileDlgOpen(self):
        """Opens a file browser dialog for selecting an image file.

        Returns:
            A file path string, or False if the dialog was cancelled.

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

    def imageTabSave(self, index=None):
        """Wrapper method for the process of saving image data.

        Args:
            index (int): Index of the ImageTab the image data of which should be
                saved. If None is passed, the method will attempt to find the
                currently selected tab.

        """

        if index == None or index == False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it == None:
            return

        dlgsave = self.imageFileDlgSave()
        if dlgsave == False:
            return

        filepath = dlgsave[0]
        splitext = os.path.splitext(dlgsave[0])
        mimetype = None
        ext = None
        for k, v in self.IMAGE_SAVE_FILTERS.items():
            if v[0] != dlgsave[1]:
                continue
            mimetype = k
            ext = v[1]
            break

        if splitext[1] == '':
            filepath += '.'+ext

        self.setStatusBarMsg('Saving image file: ' + filepath)

        if mimetype == 'image/png':
            im_dim = it.image.dimensions
            pixmap = QtGui.QPixmap(im_dim['w'], im_dim['h'])
            painter = QtGui.QPainter(pixmap)
            it._imageScene.render(painter)
            painter.end()
            pixmap.save(filepath, 'PNG')

        if mimetype == 'text/csv':
            it.image.save(filepath, imageutils.Image.FORMAT_CSV)

        self.setStatusBarMsg('Done.', 3)

    def imageFileDlgSave(self):
        """Opens a file browser dialog for saving an image file.

        Returns:
            A tuple containing a file path string and the selected mime type,
            or False if the dialog was cancelled.

        """

        dlg = QtWidgets.QFileDialog(self, 'Save image as')
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        #dlg.setMimeTypeFilters(["image/png", "text/csv"])

        filters = []
        for k, v in self.IMAGE_SAVE_FILTERS.items():
            filters.append(v[0])
        dlg.setNameFilters(filters)

        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            return (dlg.selectedFiles()[0], dlg.selectedNameFilter())
        else:
            return False

    def imageTabCreate(self, imageHandle, tabName="No image"):
        """Creates and focuses a new tab in the tab widget using the specified
        image file.

        Args:
            imageHandle: An Image() object reference (see imageutils.py).
            tabName (str): A text string to be shown as the tab label.

        Returns:
            The newly created ImageTab object.

        """

        it = ImageTab(self, self.tabWidget)
        it.open(imageHandle, tabName)
        self.imageTabs.append(it)
        return it

    def imageTabCloseDialog(self, index=None):
        """Shows a two option dialog box asking to confirm whether to close the
        image tab or not.

        Args:
            index (int): Index of the ImageTab. If None is passed, the method
                will attempt to find the currently selected tab.

        """

        if index == None or index == False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it == None:
            return

        dlg = GenericDialog()
        dlg.setText('Are you sure you want to close this tab?')
        dlg.setAccept(lambda: self.imageTabClose(index))
        dlg.show()
        dlg.exec_()

    def imageTabClose(self, index=None):
        """Closes the tab specified by the index argument.

        Args:
            index (int): Index of the ImageTab. If None is passed, the method
                will attempt to find the currently selected tab.

        """

        if index == None or index == False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it == None:
            return

        it.close()
        self.imageTabs.remove(it)

    def imageTabFind(self, index):
        """Finds the ImageTab object corresponding with the tab at specified index.

        Args:
            index (int): Index of the ImageTab to find.

        Returns:
            Returns either an ImageTab object, or None if no corresponding object
            was found.
        """

        if index == -1:
            return None

        for o in self.imageTabs:
            if o.widgetIndex == index:
                return o
        return None

    def imageTabCurrent(self):
        """Tries to return the currently selected ImageTab object.

        Returns:
            Returns either an ImageTab object, or None if no corresponding object
            was found.
        """

        return self.imageTabFind(self.tabWidget.currentIndex())

    def openAbout(self):
        """Opens the program About dialog."""

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
    """Widget container for all of the functionality and UI elements within each
    opened image tab.

    Attributes:
        layout (:obj:`Ui_MainWindow`): Object holding all the layout definitions
            for the encompassing widget inside each image tab, generated from
            the .ui files in the /devel/ directory.
        opened (bool): Is False until the open() method is called, True afterwards.
        image (:obj:Image): An object holding the image data for the image loaded
            within this tab.

    """

    def __init__(self, windowRef, tabWidgetRef):
        super().__init__()

        self.layout = ui_displot_image.Ui_ImageTabPrototype()
        self.layout.setupUi(self)

        self.opened = False
        self.image = None

        self._qImage = None
        self._qPixMap = None
        self._imageScenePixmap = None
        self._minimapScenePixmap = None
        self._window = windowRef
        self._tabWidget = tabWidgetRef

        self._regionPen = QtGui.QPen(QtGui.QColor.fromRgb(255, 0, 0))
        self._regionSelPen = QtGui.QPen(QtGui.QColor.fromRgb(255, 255, 255))
        self._regionNewPen = QtGui.QPen(QtGui.QColor.fromRgb(0, 255, 255))
        self._regionMovePen = QtGui.QPen(QtGui.QColor.fromRgb(255, 255, 0))

        self._lastPatchSize = int(
            self.findChild(QtWidgets.QSpinBox, "value_PatchSize").cleanText())
        self._movingFragment = None

        # Init main image view layout objects
        self._imageScene = QtWidgets.QGraphicsScene()
        self._imageView = self.findChild(QtWidgets.QGraphicsView, "imageView")
        self._imageView.setScene(self._imageScene)
        self._imageView.imageTab = self
        self._imageView.initEvents()
        self._imageView.regionNewPen = self._regionNewPen
        self._imageView.regionMovePen = self._regionMovePen

        # Init minimap layout objects
        self._minimapScene = QtWidgets.QGraphicsScene()
        self._minimapView = self.findChild(QtWidgets.QGraphicsView, "minimap")
        self._minimapView.setScene(self._minimapScene)
        self._minimapView.imageTab = self

        # Init list widget
        self._fragmentList = self.findChild(QtWidgets.QTableWidget, "fragmentList")
        self._fragmentList.imageTab = self
        self._fragmentList.itemSelectionChanged.connect(self._selectedFragment)

        # Init button events
        self._imageScanBtn = self.findChild(QtWidgets.QPushButton, "button_Scan")
        self._imageScanBtn.clicked.connect(self.scanImage)
        self._fragAddBtn = self.findChild(QtWidgets.QPushButton, "button_AddFrag")
        self._fragAddBtn.clicked.connect(
            lambda: self._imageView.setMouseMode(WorkImageView.MODE_REGION_NEW))
        self._imageView.clickedRegionNew.connect(self.addNewFragment)
        self._fragRemBtn = self.findChild(QtWidgets.QPushButton, "button_RemFrag")
        self._fragRemBtn.clicked.connect(self.deleteSelFragments)
        self._fragMovBtn = self.findChild(QtWidgets.QPushButton, "button_MovFrag")
        self._fragMovBtn.clicked.connect(self._moveSelFragment)
        self._imageView.clickedRegionMove.connect(self.moveFragment)

    def setTabLabel(self, label):
        """Sets the tab label to the specified text.

        Args:
            label (str): A text string to be inserted into the tab label.
        """
        self._tabWidget.setTabText(self.widgetIndex, label)

    @property
    def filePath(self):
        return self.image.filePath

    @property
    def widgetIndex(self):
        return self._tabWidget.indexOf(self)

    def open(self, imageHandle, tabName):
        """Sets up the UI for an image loaded using the Image object functionality.

        Sets the `opened` attribute to True. If said attribute has already been
        set to true, the method will exit.

        Args:
            imageHandle (:obj:`Image`): The Image object reference containing the
                loaded image.
            tabName (str): The name of the tab.

        """

        """Sets up the UI for the image referenced in imageHandle."""
        if self.opened == True:
            return
        self._tabWidget.addTab(self, tabName)
        self._tabWidget.setCurrentIndex(self.widgetIndex)

        self.image = imageHandle
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
        self._qImage = self._grayscale2QImage(self.image.data)
        self._qPixMap = QtGui.QPixmap.fromImage(self._qImage)
        if self._imageScenePixmap == None:
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

        sigma = self.findChild(QtWidgets.QDoubleSpinBox, "value_GaussianSigma")
        min_area = self.findChild(QtWidgets.QSpinBox, "value_DiscardLabels")
        margin = self.findChild(QtWidgets.QSpinBox, "value_DiscardMargins")
        patch_size = self.findChild(QtWidgets.QSpinBox, "value_PatchSize")
        d_target = self.findChild(
            QtWidgets.QDoubleSpinBox,
            "value_DissimilarityTarget"
        )
        c_target = self.findChild(
            QtWidgets.QDoubleSpinBox,
            "value_CorrelationTarget"
        )
        d_tolerance = self.findChild(
            QtWidgets.QDoubleSpinBox,
            "value_DissimilarityTolerance"
        )
        c_tolerance = self.findChild(
            QtWidgets.QDoubleSpinBox,
            "value_CorrelationTolerance"
        )

        self._window.setStatusBarMsg(
            'Scanning for dislocations... (edge detection)')

        edgeData = imageutils.edgeDetection(
            image=self.image.data,
            sigma=sigma.cleanText(),
            min_area=min_area.cleanText(),
            margin=margin.cleanText(),
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
            image=self.image.data,
            region_list=edgeData[0],
            angles=angles,
            patch_size=patch_size.cleanText(),
            targets=(d_target.cleanText(), c_target.cleanText()),
            tolerances=(d_tolerance.cleanText(), c_tolerance.cleanText())
        )

        stats = {**edgeData[1], **glcmData[1]}

        console = (
            "Edge detection found {} fragments\n"
            .format(stats['edgeDetectInitial'])
            +"{} fragments discarded due to area being less than {}\n"
            .format(stats['minAreaDiscarded'], min_area.text())
            +"{} fragments discarded due to falling within {} edge margin\n"
            .format(stats['marginDiscarded'], margin.text())
            +"{} out of {} fragments labelled\n\n"
            .format(len(edgeData[0]), stats['edgeDetectInitial'])
            +"{} fragments discarded due to patch size out of bounds with image\n"
            .format(stats['borderOverlapDiscarded'])
            +"{} fragments discarded due to not falling within set GLCM bounds\n"
            .format(stats['GLCMPropsDiscarded'])
            +"{} fragment candidates found.\n"
            .format(len(glcmData[0]))
        )
        print(console)

        self.image.regions = glcmData[0]

        patch_size_int = int(patch_size.cleanText())
        self._lastPatchSize = patch_size_int
        for frag in self.image.regions:
            frag.resize(patch_size_int, patch_size_int)
            # TODO: overlap detection goes here

        self._window.setStatusBarMsg(
            'Done. {} dislocation candidates found.'.format(len(self.image.regions)))

        for frag in self.image.regions:
            frag.initUi(
                imgScene=self._imageScene,
                imgView=self._imageView,
                minimapScene=self._minimapScene,
                minimapView=self._minimapView,
                defPen=self._regionPen,
                selPen=self._regionSelPen
            )
            frag.show()

        self._fragmentList.setDataList(self.image.regions)
        self._imageScanBtn.setEnabled(True)

    def unhighlightAllFragments(self):
        for frag in self.image.regions:
            frag.highlight(False)

    def showAllFragments(self):
        for frag in self.image.regions:
            frag.show()

    def hideAllFragments(self):
        for frag in self.image.regions:
            frag.hide()

    def addNewFragment(self, x, y):
        frag = ImageTabRegion()
        frag.setSize(x, y, self._lastPatchSize, self._lastPatchSize)
        frag.initUi(
            imgScene=self._imageScene,
            imgView=self._imageView,
            minimapScene=self._minimapScene,
            minimapView=self._minimapView,
            defPen=self._regionPen,
            selPen=self._regionSelPen
        )
        frag.show()
        self._fragmentList.addRow(frag)
        self.image.regions.append(frag)

    def _moveSelFragment(self):
        sel = self._fragmentList.selectedItems()
        if len(sel) == 0:
            self._window.setStatusBarMsg(
                'No fragment selected.'
                +' Select a fragment in the list, then click the "Mov" button.', 3)
            return

        self._movingFragment = sel[0].fragmentRef
        self._imageView.setMouseMode(WorkImageView.MODE_REGION_MOVE)

    def moveFragment(self, x, y, frag=None):
        if frag == None:
            frag = self._movingFragment
            self._movingFragment = None

        sel = self._fragmentList.selectedItems()
        self._fragmentList.updateRow(sel[0].row(), x, y)
        frag.move(x, y)
        frag.updateUi()

    def deleteSelFragments(self):
        rows = self._fragmentList.getCheckedFragments()
        for frag in rows:
            frag.fragmentRef.removeFromScene()
            self.image.regions.remove(frag.fragmentRef)
            self._fragmentList.removeRow(frag.row())

    def _selectedFragment(self):
        """A UI cleanup method that resets the mouse mode on ImageView if the
        selected fragment changes."""
        self._movingFragment = None
        self._imageView.setMouseMode(WorkImageView.MODE_NORMAL)

    def _grayscale2QImage(self, imageData):
        """Converts data from a grayscale numpy array into a QImage object for
        manipulation by Qt.

        Args:
            imageData: numpy ndarray of the image.
        """
        h, w = imageData.shape

        # Load data directly from the numpy array into QImage
        result = QtGui.QImage(imageData.data, w, h, QtGui.QImage.Format_Indexed8)
        result.ndarray = imageData

        # Set up the monochrome colour palette
        for i in range(256):
            result.setColor(i, QtGui.qRgb(i, i, i))

        return result


class ImageTabRegion(imageutils.ImageRegion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.isDrawn = False
        self.isHighlighted = False
        self.hasUi = False

        self._imageScene = None
        self._imageSceneHandle = None
        self._imageView = None
        self._minimapScene = None
        self._minimapSceneHandle = None
        self._minimapView = None
        self._regionPen = None
        self._regionSelPen = None

    def initUi(self,
    imageTab=None, imgScene=None, imgView=None,
    minimapScene=None, minimapView=None,
    defPen=None, selPen=None):
        self._imageScene = imgScene
        self._imageView = imgView
        self._minimapScene = minimapScene
        self._minimapView = minimapView
        self._regionPen = defPen
        self._regionSelPen = selPen
        self.hasUi = True

    def show(self):
        if self.isDrawn == False:
            self.updateUi()
        self._imageSceneHandle.show()
        self._minimapSceneHandle.show()

    def hide(self):
        self._imageSceneHandle.hide()
        self._minimapSceneHandle.hide()

    def highlight(self, toggle=True):
        if toggle == True:
            self._imageSceneHandle.setPen(self._regionSelPen)
            self._minimapSceneHandle.setPen(self._regionSelPen)
            self.isHighlighted = True
        else:
            self._imageSceneHandle.setPen(self._regionPen)
            self._minimapSceneHandle.setPen(self._regionPen)
            self.isHighlighted = False

    def centerOn(self):
        self._imageView.centerOn(self._imageSceneHandle)

    def removeFromScene(self):
        self._imageScene.removeItem(self._imageSceneHandle)
        self._minimapScene.removeItem(self._minimapSceneHandle)

    def updateUi(self):
        if self._imageSceneHandle == None:
            self._imageSceneHandle = self._imageScene.addRect(
                self.x, self.y, self.w, self.h, self._regionPen)
        else:
            self._imageSceneHandle.setRect(self.x, self.y, self.w, self.h)

        midpoint = self.midpoint
        offset = 1
        scale = self._minimapView.getMinimapRatio()
        self._mmCoords = (
            (midpoint[0] * scale) - offset,
            (midpoint[1] * scale) - offset,
            (offset * 2),
            (offset * 2)
        )

        if self._minimapSceneHandle == None:
            self._minimapSceneHandle = self._minimapScene.addEllipse(
                self._mmCoords[0], self._mmCoords[1],
                self._mmCoords[2], self._mmCoords[3],
                self._regionPen)
        else:
            self._minimapSceneHandle.setRect(
                self._mmCoords[0], self._mmCoords[1],
                self._mmCoords[2], self._mmCoords[3])

        self.isDrawn = True
