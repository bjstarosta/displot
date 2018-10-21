from PyQt5 import QtCore, QtGui, QtWidgets


class DisplotGraphicsView(QtWidgets.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def imageTab(self):
        return self._imageTab

    @imageTab.setter
    def imageTab(self, obj):
        if not isinstance(obj, QtWidgets.QWidget):
            raise TypeError('Value needs to be an instance of QtWidgets.QWidgets')
        self._imageTab = obj


class WorkImageView(DisplotGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.zoomLevel = 1

    def initEvents(self):
        self._zoomDial = self.imageTab.findChild(QtWidgets.QSpinBox, "zoomDial")
        self._zoomDial.valueChanged.connect(self._zoomEv)

    def zoom(self, scale):
        self.scale(1 / self.zoomLevel, 1 / self.zoomLevel)
        self.scale(scale, scale)
        self.zoomLevel = scale

    def _zoomEv(self):
        self.zoom(int(self._zoomDial.cleanText()) / 100)
        self.imageTab._minimapView.drawViewbox()

    def resizeEvent(self, e):
        if self.imageTab.opened == True:
            self.imageTab._minimapView.drawViewbox()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.imageTab._minimapView.drawViewbox()


class MinimapView(DisplotGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._mmPen = QtGui.QPen(QtGui.QColor.fromRgb(255,255,255))
        self._mmBox = False

    def getMinimapRatio(self):
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
            box_w = max_w - box_x
        if box_h > (max_h - box_y):
            box_h = max_h - box_y

        if self._mmBox == False:
            self._mmBox = self.imageTab._minimapScene.addRect(
                box_x, box_y, box_w, box_h, self._mmPen);
        else:
            self._mmBox.setRect(box_x, box_y, box_w, box_h)

    def _drawViewboxEv(self, e):
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
