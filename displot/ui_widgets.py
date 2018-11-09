from PyQt5 import QtCore, QtGui, QtWidgets


class WorkImageView(QtWidgets.QGraphicsView):
    """A QGraphicsView object responsible for the main image view of the program.

    Note that it is tightly coupled to its parent QWidget object for reasons
    of UI interaction, but the assignment of its parent object reference cannot
    happen in the layout definition portion of this program.

    Attributes:
        zoomLevel: a float value indicating the current zoom level of the scene.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.zoomLevel = 1
        self._labelX = None
        self._labelY = None

        self.setMouseTracking(True)

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidget')
        self._imageTab = obj

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

    def mouseMoveEvent(self, e):
        rect = self.getVisibleRect()
        self._labelX.setText('x:'+str(rect.x()+e.x()))
        self._labelY.setText('y:'+str(rect.y()+e.y()))

    def resizeEvent(self, e):
        if self.imageTab.opened == True:
            self.imageTab._minimapView.drawViewbox()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.imageTab._minimapView.drawViewbox()


class MinimapView(QtWidgets.QGraphicsView):
    """A QGraphicsView object responsible for displaying the loaded image minimap.

    Note that it is tightly coupled to its parent QWidget object for reasons
    of UI interaction, but the assignment of its parent object reference cannot
    happen in the layout definition portion of this program.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._mmPen = QtGui.QPen(QtGui.QColor.fromRgb(0,255,0))
        self._mmBox = False

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidget')
        self._imageTab = obj

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
        vpBox = imv.mapToScene(imv.viewport().rect()).boundingRect()
        bgPixmap = self.imageTab._minimapScenePixmap.boundingRect()

        ratio = self.getMinimapRatio()
        max_w = bgPixmap.width() * ratio
        max_h = bgPixmap.height() * ratio
        box_w = vpBox.width() * ratio
        box_h = vpBox.height() * ratio
        box_x = vpBox.x() * ratio
        box_y = vpBox.y() * ratio

        # set bounds to avoid rendering weirdness
        if (box_x + box_w) > max_w:
            box_x = max_w - box_w
        if (box_y + box_h) > max_h:
            box_y = max_h - box_h
        if box_x < 0:
            box_x = 0
        if box_y < 0:
            box_y = 0
        if box_w > (max_w - box_x):
            box_w = max_w - box_x - 1
        if box_h > (max_h - box_y):
            box_h = max_h - box_y - 1

        box_w -= 1
        box_h -= 1

        if self._mmBox == False:
            self._mmBox = self.imageTab._minimapScene.addRect(
                box_x, box_y, box_w, box_h, self._mmPen);
        else:
            self._mmBox.setRect(box_x, box_y, box_w, box_h)

    def _drawViewboxEv(self, e):
        """Method to handle and constrain minimap mouse events before passing
        them onto drawViewbox.
        """
        imv = self.imageTab._imageView
        vpBox = imv.mapToScene(imv.viewport().rect()).boundingRect()
        bgPixmap = self.imageTab._imageScenePixmap.boundingRect()
        ratio = 1 / self.getMinimapRatio()

        #x = (e.x() * ratio) - (vpBox.width() / 2)
        x = e.x() * ratio
        y = e.y() * ratio

        min_x = vpBox.width() / 2
        min_y = vpBox.height() / 2
        max_x = bgPixmap.width() - min_x
        max_y = bgPixmap.height() - min_y
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
        self.checkBoxes = []
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

        self.setRowCount(len(list))
        self.tableItems = []
        self.checkBoxes = []

        fNoEdit = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        fCenter = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter

        row = 0
        for obj in list:
            items = []
            items.append(QtWidgets.QTableWidgetItem(str(row+1)))
            items[0].fragmentRef = obj
            items[0].setFlags(fNoEdit)
            items[0].setTextAlignment(fCenter)

            items.append(QtWidgets.QTableWidgetItem(str(obj.x)))
            items.append(QtWidgets.QTableWidgetItem(str(obj.y)))

            col = 0
            for item in items:
                self.setItem(row, col, item)
                col += 1

            cb = ImageTabListCheckbox(self, items[0])
            cb.setStyleSheet("margin-left:50%; margin-right:50%;")
            self.setCellWidget(row, col, cb)
            self.checkBoxes.append(cb)

            self.tableItems.append(items)
            row += 1

        self.resizeColumnsToContents()
        self.setEnabled(True)

    def addRow(self, obj):
        pass

    def removeRow(self, row):
        pass

    def getCheckedFragments(self):
        frags = []
        for cb in self.checkBoxes:
            if cb.isChecked() == True:
                frags.append(self.item(cb.getRow(), 0))

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

    def _cellClickedEv(self, row, column):
        if column == self.lastColumn:
            if self.checkBoxes[row].isChecked() == True:
                self.checkBoxes[row].setChecked(False)
            else:
                self.checkBoxes[row].setChecked(True)

    def _itemSelectionChangedEv(self):
        self._imageTab.unhighlightAllFragments()
        sel = self.selectedItems()
        sel[0].fragmentRef.centerOn()
        sel[0].fragmentRef.highlight()


class ImageTabListCheckbox(QtWidgets.QCheckBox):

    def __init__(self, tableWidget, rowFirstWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tableWidget = tableWidget
        self.rowFirstWidget = rowFirstWidget

    def getRow(self):
        return self.tableWidget.row(self.rowFirstWidget)
