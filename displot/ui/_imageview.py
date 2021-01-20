# -*- coding: utf-8 -*-
"""displot - Image tab image view UI functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class DisplotGraphicsView(QtWidgets.QGraphicsView):
    """Common functionality for graphics views."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Find parent ImageTab
        itab = self
        while (type(itab).__name__ != 'ImageTab'
        and getattr(itab, 'parent', None) is not None):
            itab = itab.parent()

        if type(itab).__name__ != 'ImageTab':
            raise Exception("Couldn't find parent ImageTab.")
        self.itab = itab

        # Set up graphics scene
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(QtGui.QPixmap())

    def addGraphicsItem(self, ref):
        """Add graphics item to the scene corresponding to this view.

        List of defined graphics items is in ui/_imageview_symbols.py.

        Args:
            ref (QtWidgets.QGraphicsItem): Object reference.

        Returns:
            None

        """
        self.scene.addItem(ref)

    def removeGraphicsItem(self, ref):
        """Remove graphics item from the scene corresponding to this view.

        List of defined graphics items is in ui/_imageview_symbols.py.

        Args:
            ref (QtWidgets.QGraphicsItem): Object reference.

        Returns:
            None

        """
        self.scene.removeItem(ref)

    def getScenePixmap(self):
        """Return current scene and all of its graphics items as a pixmap.

        Useful for exporting to static images.

        Returns:
            QtGui.QPixmap: Scene pixmap.

        """
        scene_rect = self.scene.sceneRect()
        scene_rect_size = scene_rect.size().toSize()

        pixmap = QtGui.QPixmap(scene_rect_size)
        pixmap_rect = QtCore.QRectF(pixmap.rect())

        self.scene.render(QtGui.QPainter(pixmap), pixmap_rect, scene_rect)
        return pixmap


class WorkImageView(DisplotGraphicsView):
    """Graphical workspace object.

    Attributes:
        zoomLevel (float): Current zoom level.
        onScrollContents (QtCore.pyqtSignal): Signal that emits when
            the scrollContentsBy() method is called.

    """

    onScrollContents = QtCore.pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.zoomLevel = 1
        self.setMouseTracking(True)

    def link(self):
        """Init and link object events to other layout elements.

        Call only after layout has been constructed.

        Returns:
            None

        """
        self._zoomdial = self.itab.layout.zoomDial
        self._zoomdial.valueChanged.connect(self._zoom_ev)
        self._labelx = self.itab.layout.imageCurX
        self._labely = self.itab.layout.imageCurY
        self.onScrollContents.connect(self.itab.miniView.drawViewbox)

    def mouseSceneCoords(self, x, y):
        """Transform cursor coordinates passed by event to scene relative.

        Qt mouse event coordinates are given relative to the position of the
        widget, disregarding the position of the scene contained in the
        image view. To get the position of the mouse event on the scene we
        have to take into account the position of the visible rectangle.

        Args:
            x (int): X coordinates of the cursor as passed by Qt mouse event.
            y (int): Y coordinates of the cursor as passed by Qt mouse event.

        Returns:
            tuple: A tuple of two integers of the form (x, y).

        """
        rect = self.getVisibleRect()
        return (
            int(rect.x() + (x / self.zoomLevel)),
            int(rect.y() + (y / self.zoomLevel))
        )

    def getVisibleRect(self):
        """Return the coordinates of the scene bounding rectangle.

        Returns:
            QtCore.QRectF: Object containing visible viewport coordinates.
                See: https://het.as.utexas.edu/HET/Software/PyQt/qrectf.html

        """
        return self.mapToScene(self.viewport().geometry()).boundingRect()

    def zoom(self, scale):
        """Zoom the scene according to the scale multiplier.

        Args:
            scale (float): Scale multiplier. 1.0 is original size.

        Returns:
            None

        """
        # First the scale must be reset to the original...
        self.scale(1 / self.zoomLevel, 1 / self.zoomLevel)
        # ...then the new scale level put into place.
        self.scale(scale, scale)
        self.zoomLevel = scale

    def _zoom_ev(self):
        """Zoom QSpinBox event."""
        self.zoom(int(self._zoomdial.cleanText()) / 100)
        self.itab.miniView.drawViewbox()

    def scrollContentsBy(self, dx, dy):
        """Override of Qt method to include signal."""
        super().scrollContentsBy(dx, dy)
        self.onScrollContents.emit(dx, dy)

    # Qt5 event overrides

    def resizeEvent(self, e):
        # This ensures viewport resizes the scrollarea correctly.
        self.setSceneRect(QtCore.QRectF())

        self.itab.miniView.drawViewbox()

    def mouseMoveEvent(self, e):
        m_x, m_y = self.mouseSceneCoords(e.x(), e.y())

        # show current mouse position relative to the scene
        self._labelx.setText('x: {0}'.format(m_x))
        self._labely.setText('y: {0}'.format(m_y))

        self.itab.window.cursorMode.onMouseMove(e)

    def mousePressEvent(self, e):
        self.itab.window.cursorMode.onMousePress(e)

    def mouseReleaseEvent(self, e):
        self.itab.window.cursorMode.onMouseRelease(e)

    def leaveEvent(self, e):
        self.itab.window.cursorMode.onMouseLeave(e)


class MinimapView(DisplotGraphicsView):
    """Minimap display object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._boxpen = QtGui.QPen(QtGui.QColor.fromRgb(0, 255, 0))
        self._boxobj = None

    def getMinimapRatio(self):
        """Return scaling ratio for the minimap pixmap.

        Returns a single float representing the ideal scaling ratio for the
        minimap pixmap with regards to the full sized image. Will always return
        the smallest ratio if aspect is not preserved.

        Returns:
            float: Scaling ratio.

        """
        minimap_dim = self.rect()
        workview_pixmap = self.itab.imView.pixmap.pixmap()

        w_ratio = minimap_dim.width() / workview_pixmap.width()
        h_ratio = minimap_dim.height() / workview_pixmap.height()

        if w_ratio > h_ratio:
            return h_ratio
        else:
            return w_ratio

    def drawViewbox(self):
        """Draw box denoting image view visible area on the minimap.

        This should be called every time the visible area on the image view
        changes, it is essentially a viewbox update method.

        Returns:
            None

        """
        viewport = self.itab.imView.viewport().rect()
        viewport_box = self.itab.imView.mapToScene(viewport).boundingRect()
        pixmap = self.pixmap.boundingRect()

        ratio = self.getMinimapRatio()
        max_w = (pixmap.width() * ratio) - 1
        max_h = (pixmap.height() * ratio) - 1
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

        if self._boxobj is None:
            self._boxobj = self.scene.addRect(
                box_x, box_y, box_w, box_h, self._boxpen)
            self._boxobj.setZValue(100)
        else:
            self._boxobj.setRect(box_x, box_y, box_w, box_h)

    def drawViewboxEvent(self, e):
        """drawViewbox() event handling method.

        Args:
            e (QtWidgets.QGraphicsSceneMouseEvent): Mouse event object.

        Returns:
            None

        """
        viewport = self.itab.imView.viewport().rect()
        viewport_box = self.itab.imView.mapToScene(viewport).boundingRect()
        pixmap = self.itab.imView.pixmap.boundingRect()
        ratio = 1 / self.getMinimapRatio()

        # transform minimap click coordinates to image view coordinates
        x = e.x() * ratio
        y = e.y() * ratio

        # ensure boundaries
        min_x = viewport_box.width() / 2
        min_y = viewport_box.height() / 2
        max_x = pixmap.width() - min_x
        max_y = pixmap.height() - min_y
        if x < min_x:
            x = min_x
        if x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        if y > max_y:
            y = max_y

        self.itab.imView.centerOn(x, y)
        self.drawViewbox()

    # Qt5 event overrids

    def mousePressEvent(self, e):
        self.drawViewboxEvent(e)

    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            self.drawViewboxEvent(e)
