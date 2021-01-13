# -*- coding: utf-8 -*-
"""displot - Image tab UI functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import logging

from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_displot_image import Ui_ImageTabPrototype
from ._imagetab_table import FeatureVisibility, FeatureCheckBox
from ._imagetab_tablemodel import ImageTabTableModel
from ._imagetab_feature import ImageTabFeature
from displot import Displot

log = logging.getLogger('displot')


class ImageTab(QtWidgets.QWidget, Displot):
    """Image tab UI functionality container.

    Args:
        window (ui.DisplotUi): Main window UI object.
        tab_widget (QtWidgets.QTabWidget): Tab widget reference for the tab.
        tab_name (str): Text string to be placed on the tab.
        path (str): Path to image to load.

    Attributes:
        layout (ui.Ui_ImageTabPrototype): Layout definition object.
        image (type): Description of parameter `image`.
        tabWidget (QtWidgets.QTabWidget): Tab widget reference for the tab.
        imView (ui.WorkImageView): Main working view widget for the image.
        miniView (ui.MinimapView): Minimap widget for the image.
        window

    """

    _INFOBOX_FMT = '"{path}" [W:{w}px, H:{h}px]'

    def __init__(self, window, tab_widget, tab_name, path):
        super().__init__()

        # Construct layout
        self.layout = Ui_ImageTabPrototype()
        self.layout.setupUi(self)

        # Set up properties
        self.window = window
        self.tabWidget = tab_widget

        self.imView = self.layout.imageView
        self.miniView = self.layout.minimap
        self.featureList = self.layout.featureList

        self.featuresHidden = False

        # Set up feature list table and data model
        self.featureModel = ImageTabTableModel()
        self.featureList.itab = self
        self.featureList.setModel(self.featureModel)
        self.featureList.setItemDelegateForColumn(0,
            FeatureCheckBox(self.featureList))
        self.featureList.setColumnWidth(0, 1)
        self.featureList.setItemDelegateForColumn(1,
            FeatureVisibility(self.featureList))
        self.featureList.setColumnWidth(1, 1)
        # self.featureList.setItemDelegateForColumn(2,
        #     FeatureColour(self.featureList, self.window.styles))

        # Load data from file
        self.load_data(path)  # displot.Displot

        # Show everything
        self.updatePixmaps()
        self.imView.link()
        self.imView.show()
        self.miniView.show()
        self.miniView.drawViewbox()

        # Modify UI elements
        self.tabWidget.addTab(self, tab_name)
        self.tabWidget.setCurrentIndex(self.tabIndex)

        infobox_txt = self._INFOBOX_FMT.format(
            path=self.data_obj.image_path,
            w=self.data_obj.image_width,
            h=self.data_obj.image_height
        )
        self.layout.imageInfoLabel.setText(infobox_txt)

        cb = self.layout.value_MLModel
        for w in self.window.weights:
            cb_label = '{0} ({1})'.format(w[0], w[1])
            cb.addItem(cb_label, w)

        # Set events
        cm = self.window.cursorMode
        cm.defineEvent(self._selectFeature_ev,
            cm.MOUSE_PRESS, 'feature_select')
        cm.defineEvent(self._addFeature_ev,
            cm.MOUSE_PRESS, 'feature_new')
        cm.defineEvent(self._moveFeature_ev2,
            cm.MOUSE_PRESS, 'feature_move')

        def resetMode():
            if cm.currentMode != 'feature_select':
                cm.resetMode()

        self.featureModel.dataChanged.connect(self.updateFeatureVisibility)
        self.featureModel.dataChanged.connect(resetMode)
        # self.featureModel.rowsInserted.connect(resetMode)
        self.featureModel.rowsRemoved.connect(resetMode)

        self.layout.button_AddFrag.clicked.connect(
            lambda: cm.setMode('feature_new'))
        self.layout.button_RemFrag.clicked.connect(
            self.removeSelectedFeatures)
        self.layout.button_MovFrag.clicked.connect(
            self._moveFeature_ev)
        self.layout.button_SelectAllFrags.clicked.connect(
            self.selectToggleFeatures)

        self.layout.button_Scan.clicked.connect(
            self._detection_ev)

        self.syncFeaturesToUi()

    @property
    def tabIndex(self):
        return self.tabWidget.indexOf(self)

    @property
    def imagePath(self):
        return self.data_obj.image_path

    def setTabLabel(self, label):
        """Set the tab label to the specified text.

        Args:
            label (str): Text string to be inserted into the tab label.

        Returns:
            None

        """
        self.tabWidget.setTabText(self.tabIndex, label)

    def remove(self):
        """Remove the tab.

        Note: Does not release memory. Use the DisplotUi.imageTabClose()
        method in _mainwidow.py.

        Returns:
            None

        """
        self.tabWidget.removeTab(self.tabIndex)

    def updatePixmaps(self):
        """Update pixmaps used in the image and minimap view.

        Call this whenever the image data in the data object changes.

        Returns:
            None

        """
        qimage = grayscale_to_QImage(self.data_obj.image)
        qpixmap = QtGui.QPixmap.fromImage(qimage)

        self.imView.pixmap.setPixmap(qpixmap)
        self.imView.scene.setSceneRect(0, 0, qpixmap.width(), qpixmap.height())
        self.miniView.pixmap.setPixmap(qpixmap)
        self.miniView.pixmap.setScale(self.miniView.getMinimapRatio())

    def _selectFeature_ev(self, e):
        """Mouse event handler.

        Called when a mouse click is captured on the main image view and
        the mouse mode is 'feature_select'.

        Args:
            e (QtGui.QMouseEvent): Event object.

        Returns:
            None

        """
        selectMargin = 2
        coords = QtCore.QRectF(
            e.x() - selectMargin,
            e.y() - selectMargin,
            selectMargin * 2,
            selectMargin * 2
        )

        items = []
        for item in self.imView.scene.items(coords):
            if type(item).__name__ == 'FeatureMarker':
                items.append(item)

        for feature in self.featureModel.getModelData():
            if feature.imViewRef in items:
                if feature.isSelected is False:
                    feature.select(True)
                else:
                    feature.select(False)
                self.featureModel.notifyAllChanged()

    def selectToggleFeatures(self):
        """Toggle selection status on all features.

        All selected features will become unselected, and visa versa.

        Returns:
            None

        """
        for feature in self.featureModel.getModelData():
            if feature.isSelected is False:
                feature.select(True)
            else:
                feature.select(False)
        self.featureModel.notifyAllChanged()

    def moveFeature(self, feature, x, y):
        """Move the passed feature object in the UI and update its coordinates.

        Note: This object will not be available to the program logic until
        syncFeaturesFromUi() is called.

        Args:
            feature (ui.ImageTabFeature): Feature object to move.
            x (int): X component of the new coordinates.
            y (int): Y component of the new coordinates.

        Returns:
            None

        """
        feature.move(x, y)
        self.featureModel.notifyAllChanged()

    def _moveFeature_ev(self):
        """Button press event handler.

        Called when the move feature button is pressed on the UI.

        Returns:
            None

        """
        sel = self.featureModel.getSelectedObjects()

        if len(sel) != 1:
            if len(sel) == 0:
                msg = 'No feature selected. Select a feature in the list, '\
                    'then click the move button.'
            if len(sel) > 1:
                msg = 'More than one feature selected. Select only one '\
                    'feature in the list, then click the move button.'
            self.window.setStatusBarMsg(msg, 3000)
            return

        self.window.cursorMode.setMode('feature_move')

    def _moveFeature_ev2(self, e):
        """Mouse event handler.

        Called when a mouse click is captured on the main image view and
        the mouse mode is 'feature_move'.

        Args:
            e (QtGui.QMouseEvent): Event object.

        Returns:
            None

        """
        sel = self.featureModel.getSelectedObjects()

        if len(sel) != 1:
            return

        x, y = self.imView.mouseSceneCoords(e.x(), e.y())
        self.moveFeature(sel[0], x, y)

    def addFeature(self, feature):
        """Add the passed feature object to the UI.

        Note: This object will not be available to the program logic until
        syncFeaturesFromUi() is called.

        Args:
            feature (ui.ImageTabFeature): Feature object to add.

        Returns:
            None

        """
        row = self.featureModel.rowCount()
        self.featureModel.addDataObject(feature)
        self.featureModel.insertRows(row, 1)
        feature.show()

    def _addFeature_ev(self, e):
        """Mouse event handler.

        Called when a mouse click is captured on the main image view and
        the mouse mode is 'feature_add'.

        Args:
            e (QtGui.QMouseEvent): Event object.

        Returns:
            None

        """
        x, y = self.imView.mouseSceneCoords(e.x(), e.y())
        self.addFeature(ImageTabFeature(self, x, y))

    def removeFeature(self, feature):
        """Remove the passed feature object from the UI.

        Note: This will not be reflected in the internal program storage until
        syncFeaturesFromUi() is called.

        Args:
            feature (ui.ImageTabFeature): Feature object to add.

        Returns:
            None

        """
        row = self.featureModel.getDataObjectRow(feature)
        if row is not None:
            self.featureModel.removeRows(row, 0)
            feature.removeFromScene()

    def removeSelectedFeatures(self):
        """Remove all selected features from the UI.

        This will search for all selected/checked rows in the table, and
        remove all corresponding features and table rows.

        Note: This will not be reflected in the internal program storage until
        syncFeaturesFromUi() is called.

        Returns:
            None

        """
        sel = self.featureModel.getSelectedObjects()
        for feature in sel:
            self.removeFeature(feature)

    def removeAllFeatures(self):
        """Remove all features from the UI and reset the table model.

        Returns:
            None

        """
        for feature in self.featureModel.getModelData():
            feature.removeFromScene()
        self.featureModel.setModelData([])

    def showAllFeatures(self):
        """Set all features in the table model data to visible in the UI.

        Returns:
            None

        """
        for feature in self.featureModel.modelData:
            feature.show()
        self.featureModel.notifyAllChanged()
        self.featuresHidden = False

    def hideAllFeatures(self):
        """Set all features in the table model data to hidden in the UI.

        Returns:
            None

        """
        for feature in self.featureModel.modelData:
            feature.hide()
        self.featureModel.notifyAllChanged()
        self.featuresHidden = True

    def updateFeatureVisibility(self):
        """Update UI feature visibility based on table model data properties.

        Returns:
            None

        """
        for feature in self.featureModel.modelData:
            if feature.isHidden is True:
                feature.hide()
            else:
                feature.show()

    def unhighlightAllFeatures(self):
        """Remove highlight from all features in the current table model data.

        Returns:
            None

        """
        for feature in self.featureModel.modelData:
            feature.highlight(False)

    def syncFeaturesToUi(self):
        """Populate UI features using the internal data object.

        Returns:
            None

        """
        self.removeAllFeatures()
        for f in self.data_obj.markers:
            uif = ImageTabFeature(self)
            uif.fromParent(f)
            self.addFeature(uif)

    def syncFeaturesFromUi(self):
        """Populate the internal data object with features defined in the UI.

        Returns:
            None

        """
        self.data_obj.markers = []
        for feature in self.featureModel.modelData:
            self.data_obj.markers.append(feature.toParent())

    def _detection_ev(self):
        lt = self.layout

        weights = lt.value_MLModel.currentData()
        if weights is None:
            log.error('Could not begin: No model selected for detection. '
            'This means you probably have no models present in your '
            'displot/weights directory.')
            return

        stride = (
            int(lt.strideVerticalSpinBox.cleanText()),
            int(lt.strideHorizontalSpinBox.cleanText())
        )
        min_r = int(lt.minBlobRadiusSpinBox.cleanText())
        max_r = int(lt.maxBlobRadiusSpinBox.cleanText())

        min_sigma = int(lt.minSigmaSpinBox.cleanText())
        max_sigma = int(lt.maxSigmaSpinBox.cleanText())
        num_sigma = int(lt.numSigmaSpinBox.cleanText())
        threshold = float(lt.sigmaThresholdDoubleSpinBox.cleanText())

        td_border = int(lt.marginToleranceSpinBox.cleanText())
        td_overlap = int(lt.overlapToleranceSpinBox.cleanText())
        pred_tolerance = float(lt.predictionThresholdDoubleSpinBox.cleanText())

        self.detection(
            self.data_obj.image, weights, model='fusionnet', stride=stride,
            min_r=min_r, max_r=max_r,
            min_sigma=min_sigma, max_sigma=max_sigma,
            num_sigma=num_sigma, threshold=threshold,
            td_border=td_border, td_overlap=td_overlap,
            pred_tolerance=pred_tolerance
        )

        self.syncFeaturesToUi()


def grayscale_to_QImage(image):
    """Converts data from a grayscale numpy array into a QImage object for
    manipulation by Qt.

    Args:
        imageData: numpy ndarray of the image.
    """
    h, w = image.shape

    # Load data directly from the numpy array into QImage
    result = QtGui.QImage(image.data, w, h, w, QtGui.QImage.Format_Indexed8)
    result.ndarray = image

    # Set up the monochrome colour palette
    result.setColorCount(256)
    for i in range(256):
        result.setColor(i, QtGui.qRgb(i, i, i))

    return result
