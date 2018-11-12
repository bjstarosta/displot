# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class DisplotGraphicsView(QtWidgets.QGraphicsView):

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidget')
        self._imageTab = obj

    def drawOverlayRect(self, handle, x, y, w, h, scene_w=None, scene_h=None,
    pen=None):
        """Draws a rectangle with the specified properties onto the scene
        currently attached to the QGraphicsView.

        This function ensures that the drawn rectangle will never be out of
        existing bounds of the graphics scene, and therefore will never resize
        the graphics scene unnecessarily. The function instead draws the
        rectangle at the nearest valid coordinates.

        Args:
            handle (QGraphicsRectItem): The rectangle Qt handle. If set to None,
                the function will create and return a new Qt handle for the
                rectangle.
            x (int): X coordinate of the top-left origin of the rectangle.
            y (int): Y coordinate of the top-left origin of the rectangle.
            w (int): Desired width of the rectangle.
            h (int): Desired height of the rectangle.
            scene_w (int): Desired width of the scene. If set to None, the
                function will check the current scene size automatically.
            scene_h (int): Desired height of the scene. If set to None, the
                function will check the current scene size automatically.
            pen (QPen): The pen used to draw the rectangle.

        Returns:
            QGraphicsRectItem: The rectangle.
        """

        scene = self.scene()

        if scene_w == None:
            scene_w = scene.width()
        if scene_h == None:
            scene_h = scene.height()

        # check and set drawing bounds to avoid stretching the scene
        if (x + w) > scene_w:
            x = scene_w - w
        if (y + h) > scene_h:
            y = scene_h - h
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if w > scene_w:
            w = scene_w
        if h > scene_h:
            h = scene_h

        # this is to avoid annoying 1px stretches at the w/h boundary
        w -= 1
        h -= 1

        if handle == None:
            handle = scene.addRect(x, y, w, h, pen);
        else:
            handle.setRect(x, y, w, h)

        return handle


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
    MODE_REGION_NEW = 1
    MODE_REGION_MOVE = 2

    clickedRegionNew = QtCore.pyqtSignal(int, int, name='clickedRegionNew')
    clickedRegionMove = QtCore.pyqtSignal(int, int, name='clickedRegionMove')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mouseMode = self.MODE_NORMAL
        self.mouseGraphicsItem = None
        self.zoomLevel = 1

        self._labelX = None
        self._labelY = None

        self._regionNewHandle = None
        self._regionMoveHandle = None
        self.regionNewPen = None
        self.regionMovePen = None

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
        return (int(rect.x()+x), int(rect.y()+y))

    def initEvents(self):
        """Initialises some UI events. Run this after the image has been loaded."""
        self._zoomDial = self.imageTab.findChild(QtWidgets.QSpinBox, "zoomDial")
        self._zoomDial.valueChanged.connect(self._zoomEv)
        self._labelX = self.imageTab.findChild(QtWidgets.QLabel, "imageCurX")
        self._labelY = self.imageTab.findChild(QtWidgets.QLabel, "imageCurY")

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

        if self.mouseMode == self.MODE_REGION_NEW:
            self.clickedRegionNew.emit(m_x, m_y)
            self.setMouseMode(self.MODE_NORMAL)

        if self.mouseMode == self.MODE_REGION_MOVE:
            self.clickedRegionMove.emit(m_x, m_y)
            self.setMouseMode(self.MODE_NORMAL)

    def mouseMoveEvent(self, e):
        m_x, m_y = self.mouseCoords(e.x(), e.y())

        # show current mouse position relative to the scene
        self._labelX.setText('x:'+str(m_x))
        self._labelY.setText('y:'+str(m_y))

        psize = self.imageTab._lastPatchSize
        bg_pixmap = self.imageTab._imageScenePixmap
        if bg_pixmap == None:
            max_w = None
            max_h = None
        else:
            max_w = bg_pixmap.boundingRect().width()
            max_h = bg_pixmap.boundingRect().height()

        if self.mouseMode == self.MODE_REGION_NEW:
            self._regionNewHandle = self.drawOverlayRect(self._regionNewHandle,
                m_x, m_y, psize, psize, max_w, max_h, self.regionNewPen)

        if self.mouseMode == self.MODE_REGION_MOVE:
            self._regionMoveHandle = self.drawOverlayRect(self._regionMoveHandle,
                m_x, m_y, psize, psize, max_w, max_h, self.regionMovePen)

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

    def drawViewbox(self):
        """Draws the rectangle representing the current visible area on the
        minimap.
        """
        imv = self.imageTab._imageView
        viewport_box = imv.mapToScene(imv.viewport().rect()).boundingRect()
        bg_pixmap = self.imageTab._minimapScenePixmap.boundingRect()

        ratio = self.getMinimapRatio()
        max_w = bg_pixmap.width() * ratio
        max_h = bg_pixmap.height() * ratio
        box_w = viewport_box.width() * ratio
        box_h = viewport_box.height() * ratio
        box_x = viewport_box.x() * ratio
        box_y = viewport_box.y() * ratio

        self._mmBox = self.drawOverlayRect(self._mmBox,
            box_x, box_y, box_w, box_h, max_w, max_h, self._mmPen)

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


class ImageTabList(QtWidgets.QTableWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers = ['#', 'pos:X', 'pos:Y', ' ']
        self.headerItems = []
        self.tableItems = []
        self.lastColumn = 0

        self.cellClicked.connect(self._cellClickedEv)
        self.itemSelectionChanged.connect(self._itemSelectionChangedEv)

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidget')
        self._imageTab = obj

    def setDataList(self, list):
        self.setEnabled(False)

        if len(self.headerItems) > 0:
            self.clearContents()
        else:
            self.generateHeaders()

        #self.setRowCount(len(list))
        self.tableItems = []

        row = 0
        for obj in list:
            self.addRow(obj, row)
            row += 1

        self.resizeColumnsToContents()
        self.setEnabled(True)

    def addRow(self, obj, row=None):
        if len(self.headerItems) == 0:
            self.generateHeaders()

        if row == None:
            row = self.rowCount()

        super().insertRow(row)

        fNoEdit = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        fCenter = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        items = []
        items.append(QtWidgets.QTableWidgetItem(str(row+1)))
        items[0].fragmentRef = obj
        items[0].setFlags(fNoEdit)
        items[0].setTextAlignment(fCenter)

        items.append(QtWidgets.QTableWidgetItem(str(obj.x)))
        items.append(QtWidgets.QTableWidgetItem(str(obj.y)))
        items[1].setFlags(fNoEdit)
        items[2].setFlags(fNoEdit)

        col = 0
        for item in items:
            self.setItem(row, col, item)
            col += 1

        cb = ImageTabListCheckbox(self, items[0])
        cb.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.setCellWidget(row, col, cb)
        items.append(cb)

        self.resizeColumnsToContents()
        self.tableItems.append(items)

        return items

    def removeRow(self, row):
        cell1 = self.item(row, 0)
        for row_list in self.tableItems:
            if cell1 != row_list[0]:
                continue
            self.tableItems.remove(row_list)

        super().removeRow(row)

    def updateRow(self, row, x, y):
        cell1 = self.item(row, 0)
        row = None
        for row_list in self.tableItems:
            if cell1 != row_list[0]:
                continue
            row = row_list

        row[1].setText(str(x))
        row[2].setText(str(y))

    def getCheckedFragments(self):
        frags = []
        for item in self.tableItems:
            if item[self.lastColumn].isChecked() == True:
                frags.append(self.item(item[self.lastColumn].getRow(), 0))

        return frags

    def generateHeaders(self, headers=None):
        if type(headers) is list:
            self.headers = headers

        self.clear()
        self.setColumnCount(len(self.headers))
        self.setRowCount(0)

        self.headerItems = []
        i = 0
        for h in self.headers:
            item = QtWidgets.QTableWidgetItem(h)
            self.setHorizontalHeaderItem(i, item)
            self.headerItems.append(item)
            i += 1

        self.lastColumn = len(self.headerItems) - 1
        self.resizeColumnsToContents()

    def _cellClickedEv(self, row, column):
        row_ref = None
        cell1 = self.item(row, 0)
        for row_list in self.tableItems:
            if cell1 != row_list[0]:
                continue
            row_ref = row_list
            break

        if column == self.lastColumn:
            if row_ref[self.lastColumn].isChecked() == True:
                row_ref[self.lastColumn].setChecked(False)
            else:
                row_ref[self.lastColumn].setChecked(True)

    def _itemSelectionChangedEv(self):
        self._imageTab.unhighlightAllFragments()
        sel = self.selectedItems()
        if type(sel) is list and len(sel) > 0:
            sel[0].fragmentRef.centerOn()
            sel[0].fragmentRef.highlight()


class ImageTabListCheckbox(QtWidgets.QCheckBox):

    def __init__(self, tableWidget, rowFirstWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tableWidget = tableWidget
        self.rowFirstWidget = rowFirstWidget

    def getRow(self):
        return self.tableWidget.row(self.rowFirstWidget)
