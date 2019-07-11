# -*- coding: utf-8 -*-
import os
import sys
import gc
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from displot.ui_widgets import WorkImageView
from displot.ui_defs import ui_displot, ui_displot_about, ui_displot_dialog, ui_displot_image

import displot.imageutils as imageutils
from displot.datamodels import FeatureModel
import displot.feature as feature
from displot.config import DISPLOT_INFO


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
        imageTabFeatureStyle (:obj:`ImageTabFeatureStyle`): Style object containing
            marker pens and brushes.
        tabWidget (:obj:`QTabWidget`): Reference to the QTabWidget holding the
            opened images.
        appTitle (str): Application title as shown at the top of the window.
        appVersion (str): Application version as shown at the top of the window.
        info (dict): A dictionary holding program metadata.

    """

    IMAGE_SAVE_FILTERS = {
        'application/gzip': ['GZIP archive w/ image and feature data (*.tar.gz)', 'tar.gz'],
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
        self.imageTabFeatureStyle = ImageTabFeatureStyle()

        # Reference important UI objects
        self.tabWidget = self.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.console = self.findChild(QtWidgets.QFrame, "consoleFrame")
        self.console.initUi()

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

        self.layout.actionHideAllObjects.toggled.connect(self._imageTabToggleFeatures)
        self.layout.actionHideAllObjects.setEnabled(False)
        self.layout.actionSelectObject.toggled.connect(self._imageTabSelectFeatures)
        self.layout.actionSelectObject.setEnabled(False)
        self.layout.actionExcludeArea.toggled.connect(self._imageTabExcludeArea)
        self.layout.actionExcludeArea.setEnabled(False)
        self.layout.actionRemoveExclusion.triggered.connect(self._imageTabRemoveExclusion)
        self.layout.actionRemoveExclusion.setEnabled(False)

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

        Args:
            message (str): The message to show in the status bar.
            timeout (int): Amount of time in seconds after which the message
                will disappear. By default it's set to 0, which means the
                message will stay shown until replaced with something else.

        """

        self.statusBar().showMessage(message, timeout)

    def refreshMenus(self, selected_obj=None):
        """Makes sure menu item actions will effect the correct tab.
        """

        it = self.tabWidget.currentWidget()
        if isinstance(it, ImageTab):
            enable = True
        else:
            enable = False

        imageMenus = [
            self.layout.actionSaveImageAs,
            self.layout.actionCloseImage,
            self.layout.actionHideAllObjects,
            self.layout.actionSelectObject,
            self.layout.actionExcludeArea
        ]
        for m in imageMenus:
            m.setEnabled(enable)

        if it._imageView.mouseMode == WorkImageView.MODE_FEATURE_SELECT:
            self.layout.actionSelectObject.setChecked(True)
        else:
            self.layout.actionSelectObject.setChecked(False)

        exclusion_mousemodes = [
            WorkImageView.MODE_EXCLUDE_NEW,
            WorkImageView.MODE_EXCLUDE_DRAW,
            WorkImageView.MODE_EXCLUDE_MOVE,
            WorkImageView.MODE_EXCLUDE_RESIZE
        ]
        if it._imageView.mouseMode in exclusion_mousemodes:
            self.layout.actionExcludeArea.setChecked(True)
        else:
            self.layout.actionExcludeArea.setChecked(False)

        if type(selected_obj).__name__ == "ImageExclusionArea":
            self.layout.actionRemoveExclusion.setEnabled(True)
        else:
            self.layout.actionRemoveExclusion.setEnabled(False)

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
        imgdata = it.prepareImageData()

        if mimetype == 'image/png':
            imgdata.imageSavePng(it._imageScene, filepath)
            self.console.add_line(it.image.file_name, "Saved PNG image to " + filepath)

        elif mimetype == 'text/csv':
            imgdata.imageSaveCsv(self.info, filepath)
            self.console.add_line(it.image.file_name, "Saved CSV file to " + filepath)

        elif mimetype == 'application/gzip':
            imgdata.imageSavePackage(self.info, filepath)
            self.console.add_line(it.image.file_name, "Saved gzipped image + feature data package to " + filepath)

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

        dlg = GenericDialog(parent=self)
        dlg.setText('Changes will be unsaved. Are you sure you want to close this tab?')
        dlg.setWindowTitle('Are you sure?')
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

    def _imageTabToggleFeatures(self, toggle=True):
        """Event method."""
        curtab = self.tabWidget.currentWidget()
        if toggle == True:
            curtab.hideAllFeatures()
        else:
            curtab.showAllFeatures()

    def _imageTabSelectFeatures(self, toggle=True):
        """Event method."""
        curtab = self.tabWidget.currentWidget()
        if toggle == True:
            self.imageTabExcludeArea(False)
            curtab._imageView.setMouseMode(WorkImageView.MODE_FEATURE_SELECT)
        else:
            curtab._imageView.setMouseMode(WorkImageView.MODE_NORMAL)
        self.layout.actionSelectObject.setChecked(toggle)

    def _imageTabExcludeArea(self, toggle=True):
        """Event method."""
        curtab = self.tabWidget.currentWidget()
        if toggle == True:
            self.imageTabSelectFeatures(False)
            curtab._imageView.setMouseMode(WorkImageView.MODE_EXCLUDE_NEW)
        else:
            curtab._imageView.setMouseMode(WorkImageView.MODE_NORMAL)
            pass
        self.layout.actionExcludeArea.setChecked(toggle)

    def _imageTabRemoveExclusion(self):
        """Event method."""
        curtab = self.tabWidget.currentWidget()
        sel = None
        for i in curtab.exclusions:
            if i.is_selected():
                sel = i
        if sel is None:
            return
        curtab._imageView.destroyMarker(sel)
        curtab.exclusions.remove(sel)
        self.layout.actionRemoveExclusion.setEnabled(False)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = ui_displot_dialog.Ui_DialogBox()
        self.layout.setupUi(self)

        self.setWindowFlag(QtCore.Qt.Dialog)
        self.setWindowFlag(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

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

        self._movingFragment = None

        # Init main image view layout objects
        self._imageScene = QtWidgets.QGraphicsScene()
        self._imageView = self.findChild(QtWidgets.QGraphicsView, "imageView")
        self._imageView.setScene(self._imageScene)
        self._imageView.imageTab = self
        self._imageView.featureStyle = self._window.imageTabFeatureStyle
        self._imageView.initEvents()

        # Init minimap layout objects
        self._minimapScene = QtWidgets.QGraphicsScene()
        self._minimapView = self.findChild(QtWidgets.QGraphicsView, "minimap")
        self._minimapView.setScene(self._minimapScene)
        self._minimapView.imageTab = self

        # Init list widget
        self._featureTable = self.findChild(QtWidgets.QTableView, "fragmentList")
        self._featureTable.imageTab = self
        self._featureTable.modelDataChanged.connect(self.refreshFeatureVisibility)
        #self._featureTable.itemSelectionChanged.connect(self._selectedFeature)

        # Init button events
        self._imageScanBtn = self.findChild(QtWidgets.QPushButton, "button_Scan")
        self._imageScanBtn.clicked.connect(self.scanImage)
        self._imageClusterBtn = self.findChild(QtWidgets.QPushButton, "button_ClusterDetect")
        #self._imageClusterBtn.clicked.connect(self.scanImage)
        self._fragAddBtn = self.findChild(QtWidgets.QPushButton, "button_AddFrag")
        self._fragAddBtn.clicked.connect(
            lambda: self._imageView.setMouseMode(WorkImageView.MODE_FEATURE_NEW))
        self._imageView.clickedFeatureNew.connect(self.addNewFeature)
        self._fragRemBtn = self.findChild(QtWidgets.QPushButton, "button_RemFrag")
        self._fragRemBtn.clicked.connect(self.deleteSelFeatures)
        self._fragMovBtn = self.findChild(QtWidgets.QPushButton, "button_MovFrag")
        self._fragMovBtn.clicked.connect(self._moveSelFeature)
        self._imageView.clickedFeatureMove.connect(self.moveFeature)
        self._imageView.clickedFeatureSelect.connect(self.selectFeature)
        self._imageView.selectionChangeExclude.connect(self._window.refreshMenus)
        self._cntrFragBtn = self.findChild(QtWidgets.QPushButton, "button_AutoCenterFrags")

        self._scanMethodBtn = self.findChild(QtWidgets.QComboBox, "value_ScanMethod")
        self._scanMethodBtn.currentIndexChanged.connect(self.changeScanMethod)

        # Set up the region list data model
        self.model = FeatureModel()
        self._featureTable.setModel(self.model)

        self.exclusions = []

    def setTabLabel(self, label):
        """Sets the tab label to the specified text.

        Args:
            label (str): A text string to be inserted into the tab label.
        """
        self._tabWidget.setTabText(self.widgetIndex, label)

    @property
    def filePath(self):
        return self.image.file_path

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
        ibText = '"' + imageHandle.file_path + '"'
        ibText += ' [W:' + str(imageHandle.dimensions['w'])
        ibText += ', H:' + str(imageHandle.dimensions['h']) + ']'
        ibText += ' [' + imageHandle.file_size + ']'
        infoBox = self.findChild(QtWidgets.QLabel, "imageInfoLabel")
        infoBox.setText(ibText)

        self._window.console.add_line(self.image.file_name, "Loaded file: "+self.image.file_path)

        self.opened = True

    def close(self):
        """Destroys the tab and cleans up."""
        if self.opened == False:
            return
        self._tabWidget.removeTab(self.widgetIndex)

    def prepareImageData(self):
        """Creates and returns a populated ImageData object for saving."""
        data = imageutils.ImageData(DISPLOT_INFO)
        data.image = self.image
        data.features = self.model.getDataList()
        data.editordata['exclusions'] = self.exclusions
        return data

    def loadImageData(self, data):
        """Loads properties from an ImageData object into self, e.g. after reading
        a frozen ImageData object."""
        if data.metadata['dataVersion'] != DISPLOT_INFO['dataVersion']:
            raise ValueError('Passed data object is of a different version than this release of displot supports.')

        self.image = data.image
        self.model.setDataList(data.features)
        self._featureTable.resetView()
        #self._featureTable.resetView()

        self.exclusions = data.editordata['exclusions']

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
        self.clearAllFeatures()

        if self._scanMethodBtn.currentIndex() == 0:
            self.image.set_feature_extractor('swt4haar2')

            uicfg = {
                "value_FGMedian": QtWidgets.QSpinBox,
                "value_BGMedian": QtWidgets.QSpinBox,
                #"value_CannySigma": QtWidgets.QDoubleSpinBox,
                "value_DetailSkew": QtWidgets.QDoubleSpinBox,
                "value_MinFeatureArea": QtWidgets.QSpinBox,
                "value_MaxBboxOverlap": QtWidgets.QSpinBox,
                "value_MaxOverlap": QtWidgets.QSpinBox
            }
            for handle, type in uicfg.items():
                uicfg[handle] = self.findChild(type, handle).cleanText()

            self.image.features.FG_MEDIAN = uicfg["value_FGMedian"]
            self.image.features.BG_MEDIAN = uicfg["value_BGMedian"]
            self.image.features.L0MUL = float(uicfg["value_DetailSkew"]) / 100
            self.image.features.L1MUL = 1 - self.image.features.L0MUL
            #self.image.features.CSIGMA = uicfg["value_CannySigma"]
            self.image.features.MAX_BBOX_OVERLAP = float(uicfg["value_MaxBboxOverlap"]) / 100
            self.image.features.MAX_OVERLAP = float(uicfg["value_MaxOverlap"]) / 100
            self.image.features.MIN_FEATURE_AREA = uicfg["value_MinFeatureArea"]

        elif self._scanMethodBtn.currentIndex() == 1:
            self.image.set_feature_extractor('gradient')

            uicfg = {
                "value_FGMedian": QtWidgets.QSpinBox,
                "value_BGMedian": QtWidgets.QSpinBox,
                #"value_CannySigma": QtWidgets.QDoubleSpinBox,
            }
            for handle, type in uicfg.items():
                uicfg[handle] = self.findChild(type, handle).cleanText()

            self.image.features.FG_MEDIAN = uicfg["value_FGMedian"]
            self.image.features.BG_MEDIAN = uicfg["value_BGMedian"]
            #self.image.features.CSIGMA = uicfg["value_CannySigma"]

        # Make sure FeatureExtractor spits out lists of subclasses of Feature hooked into the UI
        if self.image.features.factory.getBaseClass() == 'Feature':
            self.image.features.factory.setBaseClass(ImageTabFeature)

        msg = 'Scanning for dislocations using ' + self.image.features.desc
        self._window.setStatusBarMsg(msg)
        self._window.console.add_line(self.image.file_name, msg)

        # Start the feature extractor
        try:
            self.image.features.run()
        except Exception as e:
            self._window.setStatusBarMsg('Error: ' + e.error())
            print(e)
            self._imageScanBtn.setEnabled(True)
            return

        # Exclude features covered by exclusion areas
        self.image.features.list = imageutils.exclude_features(self.image.features.list, self.exclusions)

        msg = 'Done. {} dislocation candidates found.'.format(len(self.image.features.list))
        self._window.setStatusBarMsg(msg)
        self._window.console.add_line(self.image.file_name, msg)

        for frag in self.image.features.list:
            frag.initUi(
                imgView=self._imageView,
                minimapView=self._minimapView,
                pen=self._window.imageTabFeatureStyle.userPens[frag.cluster_id],
                brush=self._window.imageTabFeatureStyle.userBrushes[frag.cluster_id]
            )
            frag.show()

        self.model.setDataList(self.image.features.list)
        self._featureTable.resetView()
        #self._featureTable.resetView()
        self._imageScanBtn.setEnabled(True)

    def scanClusters(self):
        pass
        # TODO: Cluster analysis
        """self._window.setStatusBarMsg(
            'Analysing clusters...')

        self.image.regions = imageutils.cluster_analysis(self.image.regions, int(centroids.cleanText()))"""

    def changeScanMethod(self, index):
        """Event method."""
        disable = [
            self.findChild(QtWidgets.QDoubleSpinBox, "value_DetailSkew")
        ]
        if index == 0:
            for el in disable:
                el.setEnabled(True)

        elif index == 1:
            for el in disable:
                el.setEnabled(False)

    def clearAllFeatures(self):
        """Permanently removes all features from the model and graphical scene."""
        for frag in self.model.modelData:
            frag.removeFromScene()
        self.model.setDataList([])
        self._imageScene.update()

    def unhighlightAllFeatures(self):
        for frag in self.model.modelData:
            frag.highlight(False)

    def refreshFeatureVisibility(self):
        for frag in self.model.modelData:
            if frag.isHidden == True:
                frag.hide()
            else:
                frag.show()

    def showAllFeatures(self):
        for frag in self.model.modelData:
            frag.show()

    def hideAllFeatures(self):
        for frag in self.model.modelData:
            frag.hide()

    def selectFeature(self, x, y):
        """Event method. Fires when mouse is clicked on the WorkImageView and
        selection mouse mode is activated."""
        coords = QtCore.QRectF(x - 2, y - 2, 4, 4)
        items = [x for x in self._imageScene.items(coords) if type(x) == QtWidgets.QGraphicsItemGroup]

        for o in self.model.getDataList():
            if o._imageSceneHandle in items:
                if o.isSelected == False:
                    o.select(True)
                else:
                    o.select(False)
                row = self.model.getDataObjectRow(o)
                self.model.notifyDataChanged(row)

    def addNewFeature(self, x, y):
        """Event method. Fires when mouse is clicked on the WorkImageView and
        add new feature mouse mode is activated."""
        frag = ImageTabFeature()
        frag.x = x
        frag.y = y

        frag.initUi(
            imgView=self._imageView,
            minimapView=self._minimapView
        )
        frag.show()

        row = self.model.rowCount()
        self.model.addDataObject(frag)
        self.model.insertRows(row, 1)
        self._featureTable.resetView()

    def _moveSelFeature(self):
        sel = self._featureTable.selectedItems()
        if sel is None:
            self._window.setStatusBarMsg(
                'No fragment selected.'
                +' Select a fragment in the list, then click the move button.', 3)
            return

        self._movingFragment = sel
        self._imageView.setMouseMode(WorkImageView.MODE_FEATURE_MOVE)

    def moveFeature(self, x, y, frag=None):
        """Event method. Fires when mouse is clicked on the WorkImageView and
        add new feature mouse mode is activated."""
        if frag == None:
            frag = self._movingFragment
            self._movingFragment = None

        frag.move(x, y)
        frag.update()
        changed_row = self.model.getDataObjectRow(frag)
        if not changed_row is None:
            self.model.notifyDataChanged(changed_row)

    def deleteSelFeatures(self):
        rows = self.model.getCheckedDataObjects()
        for frag in rows:
            row = self.model.getDataObjectRow(frag)
            if not row is None:
                self.model.removeRows(row, 1)
                frag.removeFromScene()

    def _selectedFeature(self):
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


class ImageTabFeature(feature.Feature):
    """Reimplementation of Feature that includes hooks into the UI
    representation of dislocation regions.

    Attributes:
        isDrawn (bool): True if the UI element corresponding to this region
            has been created. False otherwise.
        isHighlighted (bool): True if the UI element corresponding to this region
            has been highlighted on the QGraphicsView. False otherwise.
        isSelected (bool): True if the region's checkbox is currently selected
            in the ImageTabList widget. False otherwise.
            Note: This value does not change when simply selecting rows in
            ImageTabList, it only responds to the checkbox.
        isHighlighted (bool): True if the UI element corresponding to this region
            has been hidden on the QGraphicsView. False otherwise.
        hasUi (bool): True if the object contains the necessary UI references
            to manipulate the UI, i.e. if the initUi() method has been called.
            False otherwise.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.isDrawn = False
        self.isHighlighted = False
        self.isSelected = False
        self.isHidden = False
        self.hasUi = False

        self.currentPen = None
        self.currentBrush = None
        self._previousPen = None
        self._previousBrush = None

        self._imageSceneHandle = None
        self._imageView = None
        self._minimapSceneHandle = None
        self._minimapView = None

    def initUi(self, imageTab=None, imgView=None, minimapView=None, pen=None, brush=None):
        """Sets internal handles connecting the Feature object to the UI.

        Sets the `opened` attribute to True. If said attribute has already been
        set to true, the method will exit.

        Args:
            imageTab (:obj:`ImageTab`): The ImageTab object this Feature object belongs to.
            imgView (:obj:`QGraphicsView`): The main image view for this feature.
            minimapView (:obj:`QGraphicsView`): The minimap view for this feature.
            pen (:obj:`QPen`): The default QPen used for displaying the feature.
            brush (:obj:`QBrush`): The default QBrush used for displaying the feature.

        """
        self._imageView = imgView
        self._minimapView = minimapView

        if pen is None:
            self.currentPen = self._imageView.featureStyle.defaultPen
        else:
            self.currentPen = pen

        if brush is None:
            self.currentBrush = self._imageView.featureStyle.defaultBrush
        else:
            self.currentBrush = brush

        self.hasUi = True

    def show(self):
        """Shows the feature on the main view and the minimap if not drawn or hidden."""
        if self.isDrawn == False:
            self.update()
        self._imageSceneHandle.show()
        self._minimapSceneHandle.show()
        self.isHidden = False

    def hide(self):
        """Hides the feature on the main view and the minimap."""
        self._imageSceneHandle.hide()
        self._minimapSceneHandle.hide()
        self.isHidden = True

    def setPen(self, pen):
        """Sets the QPen currently used to draw this feature.

        Args:
            pen (:obj:`QPen`): The QPen object used to draw this feature.
        """
        self.currentPen = pen
        self.update()

    def select(self, toggle=True):
        """Selects the feature in the right-hand side table and highlights it on
        the main view.

        Args:
            toggle (bool): Passing False will unselect the feature.
        """
        if toggle == True:
            self.highlight(True)
            self.isSelected = True
        else:
            self.isSelected = False
            self.highlight(False)

    def highlight(self, toggle=True):
        """Highlights the feature on the main view in a globally defined colour.

        Args:
            toggle (bool): Passing False will dehighlight the feature.
        """
        if self.isSelected == True:
            return

        if toggle == True:
            self._previousPen = self.currentPen
            self.currentPen = self._imageView.featureStyle.highlightPen
            self.isHighlighted = True
        else:
            if self._previousPen is not None:
                self.currentPen = self._previousPen
                self._previousPen = None
            self.isHighlighted = False

        self.update()

    def centerOn(self):
        """Centres the main viewport on the feature."""
        self._imageView.centerOn(self._imageSceneHandle)

    def removeFromScene(self):
        """Removes the feature from the viewport and minimap.

        Note that this doesn't remove the feature object from the data model,
        nor the row in the table."""
        self._imageView.destroyMarker(self._imageSceneHandle)
        self._minimapView.destroyMarker(self._minimapSceneHandle)
        self._imageSceneHandle = None
        self._minimapSceneHandle = None

    def update(self):
        """Updates the scene object and the graphics view."""

        self._imageSceneHandle = self._imageView.drawMarker((self.x, self.y),
            self.currentPen, self.currentBrush, self._imageSceneHandle)

        offset = 1
        scale = self._minimapView.getMinimapRatio()

        self._minimapSceneHandle = self._minimapView.drawMarker(
            (
                (self.x * scale) - offset,
                (self.y * scale) - offset,
                (offset * 2),
                (offset * 2)
            ),
            self.currentPen, self.currentBrush, self._minimapSceneHandle)

        self.isDrawn = True


class ImageTabFeatureStyle(object):

    def __init__(self):

        self.userColours = [
            #QtGui.QColor(0x004499),
            QtGui.QColor(0xEEEE00),
            QtGui.QColor(0x00CC00),
            QtGui.QColor(0xDD0000),
            QtGui.QColor(0x6666FF),
            QtGui.QColor(0x88BB00),
            QtGui.QColor(0xFFBB00),
            QtGui.QColor(0x00BBFF),
            QtGui.QColor(0xEEEEAA)
        ]

        self.userPens = []
        self.userBrushes = []
        for c in self.userColours:
            self.userPens.append(QtGui.QPen(c))
            self.userBrushes.append(QtGui.QBrush(c))

        self.defaultPen = self.userPens[len(self.userPens)-1]
        self.defaultBrush = self.userBrushes[len(self.userBrushes)-1]
        self.highlightPen = QtGui.QPen(QtGui.QColor(0xFFFFFF))
        self.newCursorPen = QtGui.QPen(QtGui.QColor(0xF20884))
        self.moveCursorPen = QtGui.QPen(QtGui.QColor(0x02ABEA))
