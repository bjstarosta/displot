# -*- coding: utf-8 -*-
from time import localtime, strftime
from PyQt5 import QtCore, QtGui, QtWidgets

from displot.ui_defs import feathericons_rc


class DisplotGraphicsView(QtWidgets.QGraphicsView):

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidget')
        self._imageTab = obj


class WorkImageView(DisplotGraphicsView):
    """A QGraphicsView object responsible for the main image view of the program.

    Note that it is tightly coupled to its parent QWidget object for reasons
    of UI interaction, but the assignment of its parent object reference cannot
    happen in the layout definition portion of this program.

    Attributes:
        imageTab: an object reference to the tab containing the graphics view.
        zoomLevel: a float value indicating the current zoom level of the scene.
    """

    MODE_NORMAL = 0
    MODE_FEATURE_NEW = 1
    MODE_FEATURE_MOVE = 2
    MODE_FEATURE_SELECT = 3
    MODE_EXCLUDE_NEW = 4
    MODE_EXCLUDE_DRAW = 5
    MODE_EXCLUDE_MOVE = 6
    MODE_EXCLUDE_RESIZE = 7

    clickedFeatureNew = QtCore.pyqtSignal(int, int, name='clickedFeatureNew')
    clickedFeatureMove = QtCore.pyqtSignal(int, int, name='clickedFeatureMove')
    clickedFeatureSelect = QtCore.pyqtSignal(int, int, name='clickedFeatureSelect')
    mousePressExclude = QtCore.pyqtSignal(int, int, name='mousePressExclude')
    mouseReleaseExclude = QtCore.pyqtSignal(int, int, name='mouseReleaseExclude')
    selectionChangeExclude = QtCore.pyqtSignal(object, name='selectionChangeExclude')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mouseMode = self.MODE_NORMAL
        self.mouseGraphicsItem = None
        self.zoomLevel = 1
        self.featureStyle = None

        self._labelX = None
        self._labelY = None

        self._selboxHandle = None
        self._selboxPen = QtGui.QPen(QtGui.QColor.fromRgb(0,255,0))
        self._selboxBrush = QtGui.QBrush(QtGui.QColor.fromRgb(0,255,0,10))
        self._selboxOrigin = None
        self._selOrigin = None
        self._selCurrent = None
        self._regionNewHandle = None
        self._regionMoveHandle = None

        self.setMouseTracking(True)

    def setMouseMode(self, mode):
        """Sets the mouse mode for the main graphics view.

        Depending on the mouse mode the cursor will behave differently when
        interacting with the WorkImageView. The act of setting the mouse mode
        will also clean up any entities remaining from the previous mouse mode.

        Args:
            mode (int): The mode setting. Supported modes can be seen in the
                constants list of this class.

        """
        if self._regionNewHandle != None:
            self.scene().removeItem(self._regionNewHandle)
            self._regionNewHandle = None

        if self._regionMoveHandle != None:
            self.scene().removeItem(self._regionMoveHandle)
            self._regionMoveHandle = None

        self.mouseMode = mode

    def mouseCoords(self, x, y):
        rect = self.getVisibleRect()
        return (int(rect.x()+(x/self.zoomLevel)), int(rect.y()+(y/self.zoomLevel)))

    def initEvents(self):
        """Initialises some UI events. Run this after the image has been loaded."""
        self._zoomDial = self.imageTab.findChild(QtWidgets.QSpinBox, "zoomDial")
        self._zoomDial.valueChanged.connect(self._zoomEv)
        self._labelX = self.imageTab.findChild(QtWidgets.QLabel, "imageCurX")
        self._labelY = self.imageTab.findChild(QtWidgets.QLabel, "imageCurY")

    def drawMarker(self, coords, pen, brush=None, ref=None):
        """Draws a feature marker on the main view. Returns an object reference.

        Args:
            coords (tuple): A 2-tuple of ints (x, y) where x and y are
                the midpoint coordinates of the marker.
            pen (QtGui.QPen): Pen to use for drawing the object.
            brush (QtGui.QBrush): Brush to use for drawing the object.
            ref (object): Reference an existing object to update here,
                or None to create a new object.

        Returns:
            QGraphicsItem: Reference to the graphical object.

        """
        scene = self.scene()
        x, y = coords
        w, h = (10, 10)

        if ref is None:
            ref = QtWidgets.QGraphicsItemGroup()

            hline = QtWidgets.QGraphicsLineItem(0, int(h/2), w, int(h/2))
            hline.setPen(pen)
            ref.addToGroup(hline)
            vline = QtWidgets.QGraphicsLineItem(int(w/2), 0, int(w/2), h)
            vline.setPen(pen)
            ref.addToGroup(vline)

            scene.addItem(ref)
        else:
            for c in ref.childItems():
                c.setPen(pen)

        ref.setPos(int(x - w/2), int(y - h/2))
        return ref

    def destroyMarker(self, ref):
        """Destroys a feature marker on the minimap.

        Args:
            ref (object): Reference an existing marker object.
        """
        scene = self.scene()
        scene.removeItem(ref)

    def drawSelectionBox(self, x1, y1, x2, y2):
        sx = min(x1, x2)
        sy = min(y1, y2)
        ex = max(x1, x2)
        ey = max(y1, y2)
        w = ex - sx
        h = ey - sy

        scene = self.scene()
        if self._selboxHandle == None:
            self._selboxHandle = scene.addRect(sx, sy, w, h, self._selboxPen, self._selboxBrush);
        else:
            self._selboxHandle.setRect(sx, sy, w, h)

    def destroySelectionBox(self):
        if self._selboxHandle is not None:
            scene = self.scene()
            scene.removeItem(self._selboxHandle)
        self._selboxHandle = None
        self._selboxOrigin = None

    def getVisibleRect(self):
        return self.mapToScene(self.viewport().geometry()).boundingRect()

    def zoom(self, scale):
        """Zooms the scene according to the passed scale multiplier (float)."""
        self.scale(1 / self.zoomLevel, 1 / self.zoomLevel)
        self.scale(scale, scale)
        self.zoomLevel = scale

    def _zoomEv(self):
        self.zoom(int(self._zoomDial.cleanText()) / 100)
        self.imageTab._minimapView.drawViewbox()

    def mousePressEvent(self, e):
        m_x, m_y = self.mouseCoords(e.x(), e.y())

        if self.mouseMode == self.MODE_FEATURE_NEW:
            self.clickedFeatureNew.emit(m_x, m_y)
            self.setMouseMode(self.MODE_NORMAL)

        if self.mouseMode == self.MODE_FEATURE_MOVE:
            self.clickedFeatureMove.emit(m_x, m_y)
            self.setMouseMode(self.MODE_NORMAL)

        if self.mouseMode == self.MODE_FEATURE_SELECT:
            self.clickedFeatureSelect.emit(m_x, m_y)

        if self.mouseMode == self.MODE_EXCLUDE_NEW:
            selection = None
            for i in self.imageTab.exclusions:
                if selection is None and i.overlap_point(m_x, m_y) == True:
                    selection = i
                else:
                    i.setSelected(False)

            if selection == None:
                self._selboxOrigin = (m_x, m_y)
                self.setMouseMode(self.MODE_EXCLUDE_DRAW)
                self.selectionChangeExclude.emit(None)
            else:
                if selection.is_selected() == False:
                    selection.setSelected(True)
                    self.selectionChangeExclude.emit(selection)
                    return

                self._selCurrent = selection

                if selection.overlap_resizebox(m_x, m_y) == True:
                    self._selOrigin = (selection.x2 - m_x, selection.y2 - m_y)
                    self.setMouseMode(self.MODE_EXCLUDE_RESIZE)
                else:
                    self._selOrigin = (m_x - selection.x1, m_y - selection.y1)
                    self.setMouseMode(self.MODE_EXCLUDE_MOVE)

            self.mousePressExclude.emit(m_x, m_y)

    def mouseReleaseEvent(self, e):
        m_x, m_y = self.mouseCoords(e.x(), e.y())

        if self.mouseMode == self.MODE_EXCLUDE_DRAW:
            self.mouseReleaseExclude.emit(m_x, m_y)

            if self._selboxHandle is not None:
                area = ImageExclusionArea(self._selboxOrigin[0], self._selboxOrigin[1], m_x, m_y, self._imageTab.image)
                if area.is_valid() == True:
                    self.imageTab.exclusions.append(area)
                    scene = self.scene()
                    scene.addItem(area)

            self.destroySelectionBox()
            self.setMouseMode(self.MODE_EXCLUDE_NEW)

        if self.mouseMode == self.MODE_EXCLUDE_MOVE:
            self._selOrigin = None
            self._selCurrent = None
            self.setMouseMode(self.MODE_EXCLUDE_NEW)

        if self.mouseMode == self.MODE_EXCLUDE_RESIZE:
            self._selOrigin = None
            self._selCurrent = None
            self.setMouseMode(self.MODE_EXCLUDE_NEW)

    def mouseMoveEvent(self, e):
        m_x, m_y = self.mouseCoords(e.x(), e.y())

        # show current mouse position relative to the scene
        self._labelX.setText('x:'+str(m_x))
        self._labelY.setText('y:'+str(m_y))

        bg_pixmap = self.imageTab._imageScenePixmap
        if bg_pixmap == None:
            max_w = None
            max_h = None
        else:
            max_w = bg_pixmap.boundingRect().width()
            max_h = bg_pixmap.boundingRect().height()

        if self.mouseMode == self.MODE_FEATURE_NEW:
            self._regionNewHandle = self.drawMarker(
                (m_x, m_y),
                self.featureStyle.newCursorPen, None,
                self._regionNewHandle
            )

        if self.mouseMode == self.MODE_FEATURE_MOVE:
            self._regionMoveHandle = self.drawMarker(
                (m_x, m_y),
                self.featureStyle.moveCursorPen, None,
                self._regionMoveHandle
            )

        if self.mouseMode == self.MODE_EXCLUDE_DRAW:
            self.drawSelectionBox(
                self._selboxOrigin[0], self._selboxOrigin[1], m_x, m_y
            )

        if self.mouseMode == self.MODE_EXCLUDE_MOVE:
            self._selCurrent.move(
                m_x - self._selOrigin[0],
                m_y - self._selOrigin[1]
            )

        if self.mouseMode == self.MODE_EXCLUDE_RESIZE:
            self._selCurrent.resize(
                m_x + self._selOrigin[0],
                m_y + self._selOrigin[1]
            )

    def resizeEvent(self, e):
        if self.imageTab.opened == True:
            self.imageTab._minimapView.drawViewbox()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.imageTab._minimapView.drawViewbox()


class MinimapView(DisplotGraphicsView):
    """A QGraphicsView object responsible for displaying the loaded image minimap.

    Note that it is tightly coupled to its parent QWidget object for reasons
    of UI interaction, but the assignment of its parent object reference cannot
    happen in the layout definition portion of this program.

    Attributes:
        imageTab: an object reference to the tab containing the graphics view.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._mmPen = QtGui.QPen(QtGui.QColor.fromRgb(0,255,0))
        self._mmBox = None

    def getMinimapRatio(self):
        """Returns a single float representing the ideal scaling ratio for the
        minimap pixmap with regards to the full sized image. Will always return
        the smallest ratio if aspect is not preserved.
        """
        imh = self.imageTab._qImage

        w_ratio = self.rect().width() / imh.width()
        h_ratio = self.rect().height() / imh.height()
        if w_ratio > h_ratio:
            return h_ratio
        else:
            return w_ratio

    def getImageRatio(self):
        """Returns a tuple containing the horizontal and vertical scaling ratios
        of the minimap scene view with regards to the full sized image.

        Generally both scaling ratios should be the same, but if aspect ratio
        was not preserved for some reason then they won't be.
        """
        return self.transform().m11(), self.transform().m22()

    def drawMarker(self, coords, pen, brush=None, ref=None):
        """Draws a feature marker on the minimap. Returns an object reference.

        Args:
            coords (tuple): A 4-tuple of ints (x, y, w, h) where x and y are
                the upper left corner coordinates of the marker and w and h are
                its desired width and height.
            pen (QtGui.QPen): Pen to use for drawing the object.
            brush (QtGui.QBrush): Brush to use for drawing the object.
            ref (object): Reference an existing object to update here,
                or None to create a new object.

        Returns:
            QGraphicsItem: Reference to the graphical object.

        """
        scene = self.scene()
        x, y, w, h = coords

        if ref is None:
            ref = scene.addEllipse(x, y, w, h, pen, brush)
        else:
            ref.setRect(x, y, w, h)

        return ref

    def destroyMarker(self, ref):
        """Destroys a feature marker on the minimap.

        Args:
            ref (object): Reference an existing marker object.
        """
        scene = self.scene()
        scene.removeItem(ref)

    def drawViewbox(self):
        """Draws the rectangle representing the current visible area on the
        minimap.
        """
        imv = self.imageTab._imageView
        viewport_box = imv.mapToScene(imv.viewport().rect()).boundingRect()
        bg_pixmap = self.imageTab._minimapScenePixmap.boundingRect()

        ratio = self.getMinimapRatio()
        max_w = (bg_pixmap.width() * ratio) - 1
        max_h = (bg_pixmap.height() * ratio) - 1
        box_w = viewport_box.width() * ratio
        box_h = viewport_box.height() * ratio
        box_x = viewport_box.x() * ratio
        box_y = viewport_box.y() * ratio

        # check and set drawing bounds to avoid stretching the scene
        if (box_x + box_w) > max_w:
            box_x = max_w - box_w
        if (box_y + box_h) > max_h:
            box_y = max_h - box_h
        if box_x < 0:
            box_x = 0
        if box_y < 0:
            box_y = 0
        if box_w > max_w:
            box_w = max_w
        if box_h > max_h:
            box_h = max_h

        scene = self.scene()
        if self._mmBox == None:
            self._mmBox = scene.addRect(box_x, box_y, box_w, box_h, self._mmPen);
        else:
            self._mmBox.setRect(box_x, box_y, box_w, box_h)

    def _drawViewboxEv(self, e):
        """Method to handle minimap mouse events before centering the viewport
        and passing the overlay draw calls.
        """
        imv = self.imageTab._imageView
        viewport_box = imv.mapToScene(imv.viewport().rect()).boundingRect()
        bg_pixmap = self.imageTab._imageScenePixmap.boundingRect()
        ratio = 1 / self.getMinimapRatio()

        #x = (e.x() * ratio) - (viewport_box.width() / 2)
        x = e.x() * ratio
        y = e.y() * ratio

        min_x = viewport_box.width() / 2
        min_y = viewport_box.height() / 2
        max_x = bg_pixmap.width() - min_x
        max_y = bg_pixmap.height() - min_y
        if x < min_x:
            x = min_x
        if x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        if y > max_y:
            y = max_y

        imv.centerOn(x, y)
        self.drawViewbox()

    def mousePressEvent(self, e):
        self._drawViewboxEv(e)

    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            self._drawViewboxEv(e)


class ImageExclusionArea(QtWidgets.QGraphicsItem):

    def __init__(self, x1, y1, x2, y2, image):
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            raise ValueError('Argument values cannot be negative ('+str([x1, y1, x2, y2])+')')

        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)

        self.resizeBoxOffset = 12

        self._selected = False
        self._image = image

        super().__init__()

        #self.setPanelModality(QtWidgets.QGraphicsItem.SceneModal)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self._set_brect()

    @property
    def width(self):
        return self.x2 - self.x1

    @width.setter
    def width(self, w):
        if w < int(self.resizeBoxOffset * 1.5):
            w = int(self.resizeBoxOffset * 1.5)
        self.x2 = self.x1 + w

    @property
    def height(self):
        return self.y2 - self.y1

    @height.setter
    def height(self, h):
        if h < int(self.resizeBoxOffset * 1.5):
            h = int(self.resizeBoxOffset * 1.5)
        self.y2 = self.y1 + h

    @property
    def area(self):
        return self.width * self.height

    def move(self, x1, y1):
        if x1 < 0:
            self.x2 = self.width
            self.x1 = 0
        elif x1 > (self._image.width - self.width):
            self.x2 = self._image.width
            self.x1 = self._image.width - self.width
        else:
            self.x2 = x1 + self.width
            self.x1 = x1

        if y1 < 0:
            self.y2 = self.height
            self.y1 = 0
        elif y1 > (self._image.height - self.height):
            self.y2 = self._image.height
            self.y1 = self._image.height - self.height
        else:
            self.y2 = y1 + self.height
            self.y1 = y1

        self._set_brect()

    def resize(self, x2, y2):
        if (x2 - self.x1) < int(self.resizeBoxOffset * 1.5):
            self.x2 = self.x1 + int(self.resizeBoxOffset * 1.5)
        elif x2 >= self._image.width:
            self.x2 = self._image.width
        else:
            self.x2 = x2

        if (y2 - self.y1) < int(self.resizeBoxOffset * 1.5):
            self.y2 = self.y1 + int(self.resizeBoxOffset * 1.5)
        elif y2 >= self._image.height:
            self.y2 = self._image.height
        else:
            self.y2 = y2

        self._set_brect()

    def overlap_point(self, x, y):
        if (x >= self.x1 and x <= self.x2) and (y >= self.y1 and y <= self.y2):
            return True
        else:
            return False

    def overlap_rect(self, x1, y1, x2, y2):
        ix1 = max(x1, self.x1)
        iy1 = max(y1, self.y1)
        ix2 = min(x2, self.x2)
        iy2 = min(y2, self.y2)
        intr = (ix1 - ix2, iy1 - iy2)
        if intr[0] < 1 or intr[1] < 1:
            return False
        else:
            return True

    def overlap_resizebox(self, x, y):
        c = (self.x2 - self.resizeBoxOffset, self.y2 - self.resizeBoxOffset, self.x2, self.y2)
        if (x >= c[0] and x <= c[2]) and (y >= c[1] and y <= c[3]):
            return True
        else:
            return False

    def _set_brect(self):
        self.prepareGeometryChange()
        self._brect = QtCore.QRectF(self.x1, self.y1, self.width, self.height)

    def is_selected(self):
        return self._selected

    def is_valid(self):
        return self.width >= self.resizeBoxOffset and self.height >= self.resizeBoxOffset

    # Qt5 overrides
    def setSelected(self, enable=True):
        self._selected = enable
        super().setSelected(enable)
        self.update()

    def boundingRect(self):
        return self._brect

    def paint(self, painter, option, widget):
        rect = self.boundingRect()

        pen_nrm = QtGui.QPen(QtGui.QColor.fromRgb(255,25,25))
        pen_sel = QtGui.QPen(QtGui.QColor.fromRgb(255,155,25))
        brush_nrm = QtGui.QBrush(QtGui.QColor.fromRgb(255,25,25,20))
        brush_sel = QtGui.QBrush(QtGui.QColor.fromRgb(255,155,25,20))
        pen_resizeBox = QtGui.QPen(QtGui.QColor.fromRgb(255,155,25))
        brush_resizeBox = QtGui.QBrush(QtGui.QColor.fromRgb(255,155,25))
        icon_resizeBox = QtGui.QPixmap(":/feathericons/vendor/feather/icons/crop.svg")
        rect_resizeBox = QtCore.QRect(
            self.x2 - self.resizeBoxOffset,
            self.y2 - self.resizeBoxOffset,
            self.resizeBoxOffset,
            self.resizeBoxOffset
        )

        if self._selected == True:
            painter.setPen(pen_sel)
            painter.setBrush(brush_sel)
            painter.drawRect(rect)

            painter.setPen(pen_resizeBox)
            painter.setBrush(brush_resizeBox)
            painter.drawRect(rect_resizeBox)
            painter.drawPixmap(rect_resizeBox, icon_resizeBox)
        else:
            painter.setPen(pen_nrm)
            painter.setBrush(brush_nrm)
            painter.drawRect(rect)

        self.setZValue(1000)


class ImageTabList(QtWidgets.QTableView):
    """Custom TableView implementation for the dislocation list on each image tab.

    """

    modelDataChanged = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._imageTab = None

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidget')
        self._imageTab = obj

    def setModel(self, model):
        model.dataChanged.connect(lambda: self.modelDataChanged.emit())
        super().setModel(model)
        self.resetView()
        self.setItemDelegateForColumn(2, ImageTabListFragColour(self, self.imageTab._window.imageTabFeatureStyle))
        self.setItemDelegateForColumn(3, ImageTabListFragVisibility(self))
        self.setItemDelegateForColumn(4, ImageTabListCheckBox(self))

    def resetView(self):
        """Resets the table column width and adjusts header settings.

        """
        hheader = self.horizontalHeader()
        hheader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.resizeRowsToContents()

        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 22)
        self.setColumnWidth(3, 22)
        self.setColumnWidth(4, 22)

    def selectedItems(self):
        ind = self.selectedIndexes()
        model = self.model()
        if len(ind) > 0:
            return model.getDataObject(ind[0].row())
        return None

    def selectionChanged(self, selected, deselected):
        if not self._imageTab is None:
            self._imageTab._cntrFragBtn
            self._imageTab.unhighlightAllFeatures()
            sel = self.selectedItems()
            if not sel is None:
                if self._imageTab._cntrFragBtn.isChecked() == True:
                    sel.centerOn()
                sel.highlight()

        super().selectionChanged(selected, deselected)

    def mousePressEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            index = self.indexAt(e.pos())
            if index.column() == 2:
                self.edit(index)
        super().mousePressEvent(e)


class ImageTabListFragColour(QtWidgets.QItemDelegate):

    def __init__(self, parent, style, *args, **kwargs):
        self._featureStyle = style
        self._colorIcons = []
        self._cb = None

        for pen in self._featureStyle.userPens:
            pixmap = QtGui.QPixmap(12, 12)
            pixmap.fill(pen.color())
            self._colorIcons.append(QtGui.QIcon(pixmap))

        super().__init__(parent, *args, **kwargs)

    def paint(self, painter, option, index):
        painter.save()

        #pen = index.data(QtCore.Qt.DecorationRole)
        pen = self._featureStyle.userPens[index.data(QtCore.Qt.DisplayRole)]
        pixmap = QtGui.QPixmap(option.rect.width(), option.rect.height())
        pixmap.fill(pen.color())
        painter.drawPixmap(option.rect.x(), option.rect.y(), pixmap)
        super().drawFocus(painter, option, option.rect)

        painter.restore()
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if index.column() != 2:
            return super().createEditor(parent, option, index)

        self._cb = QtWidgets.QComboBox(parent)
        for icon in self._colorIcons:
            self._cb.addItem(icon, "")
        self._cb.currentIndexChanged.connect(self.commitAndSaveData)
        self._cb.showPopup()

        return self._cb

    def setEditorData(self, editor, index):
        if editor == None:
            return super().setEditorData(editor, index)

        currentPen = index.data(QtCore.Qt.DecorationRole)
        #boxIndex = self._featureStyle.userPens.index(currentPen)
        boxIndex = index.data(QtCore.Qt.DisplayRole)
        if boxIndex >= 0:
            editor.setCurrentIndex(boxIndex)

    def setModelData(self, editor, model, index):
        if editor == None:
            return super().setEditorData(editor, model, index)

        newPen = self._featureStyle.userPens[editor.currentIndex()]
        model.setData(index, newPen, QtCore.Qt.DecorationRole)
        model.setData(index, editor.currentIndex(), QtCore.Qt.EditRole)

    def commitAndSaveData(self):
        self.commitData.emit(self._cb)
        self.closeEditor.emit(self._cb)


class ImageTabListFragVisibility(QtWidgets.QItemDelegate):
    """Delegate class for the individual item visibility checkbox.

    See http://doc.qt.io/qt-5/qitemdelegate.html for a detailed description
    of reimplemented functions.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap(":/feathericons/vendor/feather/icons/eye-off.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.icon.addPixmap(
            QtGui.QPixmap(":/feathericons/vendor/feather/icons/eye.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.iconSize = 14

    def paint(self, painter, option, index):
        painter.save()

        if index.data(QtCore.Qt.DecorationRole) == True:
            state = QtGui.QIcon.On
        else:
            state = QtGui.QIcon.Off

        pixmap = self.icon.pixmap(self.iconSize, self.iconSize, QtGui.QIcon.Normal, state)
        xy = (
            option.rect.x() + (option.rect.width() / 2) - (self.iconSize / 2),
            option.rect.y() + (option.rect.height() / 2) - (self.iconSize / 2)
        )
        painter.drawPixmap(xy[0], xy[1], pixmap)
        super().drawFocus(painter, option, option.rect)

        painter.restore()
        super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if index.data(QtCore.Qt.DecorationRole) == True:
            state = False
        else:
            state = True

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            return model.setData(index, state, QtCore.Qt.DecorationRole)
        else:
            return False


class ImageTabListCheckBox(QtWidgets.QItemDelegate):
    """Delegate class for the persistent checkbox selection.

    See http://doc.qt.io/qt-5/qitemdelegate.html for a detailed description
    of reimplemented functions.

    """

    def paint(self, painter, option, index):
        if index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
            state = QtCore.Qt.Checked
        else:
            state = QtCore.Qt.Unchecked

        #super().drawCheck(painter, option, option.rect, state)
        super().drawFocus(painter, option, option.rect)
        super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
            state = QtCore.Qt.Unchecked
        else:
            state = QtCore.Qt.Checked

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            return model.setData(index, state, QtCore.Qt.CheckStateRole)
        else:
            return False


class Console(QtWidgets.QFrame):

    _HTMLBEGIN = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\
        <html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\
        p, li \{ white-space: pre-wrap; \}\
        </style></head><body style=\"font-family:'Roboto'; font-size:10pt; font-weight:400; font-style:normal;\">"
    _HTMLEND = "</body></html>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._toggleButton = None
        self._textBox = None
        self._lines = []

    def initUi(self):
        self._toggleButton = self.findChild(QtWidgets.QPushButton, "consoleTitleLabel")
        self._textBox = self.findChild(QtWidgets.QTextEdit, "consoleTextBox")

        self._toggleButton.clicked.connect(self.toggle)
        self._textBox.hide()

    def toggle(self):
        if self._textBox.isVisible() == True:
            self._textBox.hide()
        else:
            self._textBox.show()

    def add_line(self, filename, text):
        self._lines.append((strftime("%Y-%m-%d %H:%M:%S", localtime()), filename, text))
        self.update()

    def update(self):
        html = self._HTMLBEGIN
        for l in self._lines:
            html += "<b>["+l[0]+"]</b> (<i>"+l[1]+"</i>) "+l[2]+"<br>"
        html += self._HTMLEND
        self._textBox.setHtml(html)

        vscroll = self._textBox.verticalScrollBar()
        vscroll.setValue(vscroll.maximum())
