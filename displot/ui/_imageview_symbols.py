# -*- coding: utf-8 -*-
"""displot - Image tab image view symbols functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import math
from PyQt5 import QtCore, QtGui, QtWidgets


class DisplotSymbol(QtWidgets.QGraphicsItem):
    pass


class DisplotSymbolRect(DisplotSymbol):
    """Class containing helper methods for rectangular Qt graphics objects.

    Does not contain any painter definitions, actual objects should inherit
    from this class as necessary.

    Args:
        x1 (int): X component of the upper left corner of the rectangle.
        y1 (int): Y component of the upper left corner of the rectangle.
        x2 (int): X component of the bottom right corner of the rectangle.
        y2 (int): Y component of the bottom right corner of the rectangle.
        max_x (int): Maximum allowed X value. Infinity by default.
        max_y (int): Maximum allowed Y value. Infinity by default.

    """

    def __init__(self, x1=0, y1=0, x2=0, y2=0, max_x=math.inf, max_y=math.inf):
        super().__init__()

        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
        self.max_x = max_x
        self.max_y = max_y

        self.boundingRect = None
        self._updateBoundingRect()

    @property
    def width(self):
        return self.x2 - self.x1

    @width.setter
    def width(self, w):
        self.x2 = self.x1 + w

    @property
    def height(self):
        return self.y2 - self.y1

    @height.setter
    def height(self, h):
        self.y2 = self.y1 + h

    @property
    def area(self):
        return self.width * self.height

    def move(self, x1, y1):
        """Move rectangle to new coordinates.

        The coordinates reflect the upper left corner point of the rectangle.
        The bounding box of the rectangle will always stay fully within the
        defined scene. I.e. negative coordinates will be clipped to zero,
        and coordinates greater than max_x/max_y will be clipped to those
        values.

        Args:
            x1 (int): X component of new position of the upper left corner.
            y1 (int): Y component of new position of the upper left corner.

        Returns:
            None

        """
        if x1 < 0:
            self.x2 = self.width
            self.x1 = 0
        elif x1 > (self.max_x - self.width):
            self.x2 = self.max_x
            self.x1 = self.max_x - self.width
        else:
            self.x2 = x1 + self.width
            self.x1 = x1

        if y1 < 0:
            self.y2 = self.height
            self.y1 = 0
        elif y1 > (self.max_y - self.height):
            self.y2 = self.max_y
            self.y1 = self.max_y - self.height
        else:
            self.y2 = y1 + self.height
            self.y1 = y1

        self._updateBoundingRect()

    def resize(self, x2, y2):
        """Resize rectangle by changing coordinates of the bottom right corner.

        Args:
            x2 (int): X component of new position of the bottom right corner.
            y2 (int): Y component of new position of the bottom right corner.

        Returns:
            None

        """
        if (x2 - self.x1) < 0:
            self.x2 = self.x1
        elif x2 >= self.max_x:
            self.x2 = self.max_x
        else:
            self.x2 = x2

        if (y2 - self.y1) < 0:
            self.y2 = self.y1
        elif y2 >= self.max_y:
            self.y2 = self.max_y
        else:
            self.y2 = y2

        self._updateBoundingRect()

    def overlapsPoint(self, x, y):
        """Test if rectangle overlaps the specified point.

        Args:
            x (int): X component of the tested point.
            y (int): Y component of the tested point.

        Returns:
            bool: True if there is overlap, False otherwise.

        """
        return (
            (x >= self.x1 and x <= self.x2)
            and (y >= self.y1 and y <= self.y2)
        )

    def overlapsRect(self, x1, y1, x2, y2):
        """Test if rectangle overlaps any point on another rectangle.

        Args:
            x1 (int): X component of upper left corner of tested rectangle.
            y1 (int): Y component of upper left corner of tested rectangle.
            x2 (int): X component of bottom right corner of tested rectangle.
            y2 (int): Y component of bottom right corner of tested rectangle.

        Returns:
            bool: True if there is overlap, False otherwise.

        """
        ix1 = max(x1, self.x1)
        iy1 = max(y1, self.y1)
        ix2 = min(x2, self.x2)
        iy2 = min(y2, self.y2)
        intr = (ix1 - ix2, iy1 - iy2)
        return (intr[0] >= 1 or intr[1] >= 1)

    def _updateBoundingRect(self):
        """Update bounding rectangle of object.

        Needs to be done for Qt5 object drawing reasons.

        Returns:
            None

        """
        self.prepareGeometryChange()
        self.boundingRect = QtCore.QRectF(
            self.x1, self.y1, self.width, self.height)

    def boundingRect(self):
        """Qt5 override.

        Needs to be implemented for Qt5 object drawing reasons.

        Returns:
            QtCore.QRectF: Bounding rectangle of object.

        """
        return self.boundingRect


class SelectionBox(DisplotSymbolRect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.penNormal = QtGui.QPen(QtGui.QColor.fromRgb(0, 0, 220))
        self.brushNormal = QtGui.QBrush(QtGui.QColor.fromRgb(0, 0, 180, 64))

    def paint(self, painter, option, widget):
        painter.setPen(self.penNormal)
        painter.setBrush(self.brushNormal)
        painter.drawRect(self.boundingRect)
        self.setZValue(1001)


class ExclusionBox(DisplotSymbolRect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.penNormal = QtGui.QPen(QtGui.QColor.fromRgb(255, 25, 25))
        self.brushNormal = QtGui.QBrush(
            QtGui.QColor.fromRgb(255, 25, 25, 20))
        self.penSelected = QtGui.QPen(QtGui.QColor.fromRgb(255, 155, 25))
        self.brushSelected = QtGui.QBrush(
            QtGui.QColor.fromRgb(255, 155, 25, 20))
        self.penResizeBox = QtGui.QPen(QtGui.QColor.fromRgb(255, 155, 25))
        self.brushResizeBox = QtGui.QBrush(QtGui.QColor.fromRgb(255, 155, 25))
        self.iconResizeBox = QtGui.QPixmap(
            ":/feathericons/3rdparty/feather/icons/crop.svg")
        self.resizeBoxWidth = 12
        self.selected = False

    """@property
    def width(self):
        return super().width

    @width.setter
    def width(self, w):
        if w < int(self.resizeBoxWidth):
            w = int(self.resizeBoxWidth)
        super(ExclusionBox, self.__class__).width.fset(self, w)"""

    @DisplotSymbolRect.width.setter
    def width(self, w):
        if w < int(self.resizeBoxWidth):
            w = int(self.resizeBoxWidth)
        self.x2 = self.x1 + w

    @DisplotSymbolRect.height.setter
    def height(self, h):
        if h < int(self.resizeBoxWidth):
            h = int(self.resizeBoxWidth)
        self.y2 = self.y1 + h

    def resize(self, x2, y2):
        if x2 < self.resizeBoxWidth:
            x2 = self.resizeBoxWidth
        if y2 < self.resizeBoxWidth:
            y2 = self.resizeBoxWidth
        super().resize(x2, y2)

    # Qt5 overrides
    def setSelected(self, enable=True):
        self.selected = enable
        super().setSelected(enable)
        self.update()

    def paint(self, painter, option, widget):
        if self.selected is True:
            painter.setPen(self.penSelected)
            painter.setBrush(self.brushSelected)
            painter.drawRect(self.boundingRect)

            painter.setPen(self.penResizeBox)
            painter.setBrush(self.brushResizeBox)
            resizeBox = QtCore.QRect(
                self.x2 - self.resizeBoxWidth,
                self.y2 - self.resizeBoxWidth,
                self.resizeBoxWidth,
                self.resizeBoxWidth
            )
            painter.drawRect(resizeBox)
            painter.drawPixmap(resizeBox, self.iconResizeBox)
        else:
            painter.setPen(self.penNormal)
            painter.setBrush(self.brushNormal)
            painter.drawRect(self.boundingRect)

        self.setZValue(1000)


class FeatureMarker(DisplotSymbolRect):
    """Work image view GUI representation of a Displot feature.

    Attributes:
        r (int): Radius of the marker circle.
        textSize (int): Text font size in pixels.
        text (str): Text to render below the marker circle.
        ellipseRect (QtCore.QRectF): Marker circle bounding box and
            relative position.
        textRect (QtCore.QRectF): Text bounding box and relative position.
        penNormal (QtGui.QPen): Pen used to draw the marker circle.
        penText (QtGui.QPen): Pen used for the text colour.
        penTextShadow (QtGui.QPen): Pen used for the shadow under the text.

    """

    def __init__(self):
        self.r = 14
        self.textSize = 10
        self.text = None

        self.ellipseRect = QtCore.QRectF(0, 0, self.r, self.r)
        self.textRect = QtCore.QRectF(0, self.r, 30, self.textSize + 2)
        if self.textRect.width() > self.ellipseRect.width():
            xc = (self.textRect.width() / 2) - (self.ellipseRect.width() / 2)
            self.ellipseRect.moveTo(int(xc), 0)

        x2 = max(self.textRect.width(), self.ellipseRect.width())
        y2 = self.textRect.height() + self.ellipseRect.height()

        super().__init__(x1=0, y1=0, x2=x2, y2=y2)

        self.penNormal = QtGui.QPen(QtGui.QColor.fromRgb(255, 255, 255))
        self.penNormal.setWidth(3)
        self.penText = QtGui.QPen(QtGui.QColor.fromRgb(255, 255, 255))
        self.penTextShadow = QtGui.QPen(QtGui.QColor.fromRgb(30, 30, 30, 192))

    def setTextValue(self, text):
        self.text = text
        # self.update()  # update the QGraphicsItem manually!

    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(self.penNormal)
        painter.drawEllipse(self.ellipseRect)

        font = painter.font()
        font.setPixelSize(self.textSize)
        painter.setFont(font)
        painter.setPen(self.penTextShadow)
        painter.drawText(self.textRect.adjusted(1, 1, 0, 0),
            QtCore.Qt.AlignHCenter, self.text)
        painter.setPen(self.penText)
        painter.drawText(self.textRect,
            QtCore.Qt.AlignHCenter, self.text)

        self.setZValue(10)


class FeatureMarkerMini(DisplotSymbolRect):
    """Minimap view GUI representation of a Displot feature.

    Attributes:
        r (int): Radius of the marker circle.
        penNormal (QtGui.QPen): Pen used to draw the marker circle.

    """

    def __init__(self):
        self.r = 2
        super().__init__(x1=0, y1=0, x2=self.r, y2=self.r)

        self.penNormal = QtGui.QPen(QtGui.QColor.fromRgb(255, 255, 255))
        self.penNormal.setWidth(1)

    def paint(self, painter, option, widget):
        painter.setRenderHint(painter.Antialiasing)
        painter.setPen(self.penNormal)
        painter.drawEllipse(self.boundingRect)
        self.setZValue(10)
