# -*- coding: utf-8 -*-
"""displot - Image tab cursor functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtCore
from ._cursormode import CursorMode
from ._imageview_symbols import FeatureMarker


class ImageTabCursors(QtCore.QObject):

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.cursorMode = window.cursorMode
        self._cursor = None

        self.cursorMode.modeChanged.connect(self.clearCursor)

        self.cursorMode.defineEvent(self.featureNew,
            CursorMode.MOUSE_MOVE, 'feature_new')
        self.cursorMode.defineEvent(self.clearCursor,
            CursorMode.MOUSE_LEAVE, 'feature_new')

        self.cursorMode.defineEvent(self.featureMove,
            CursorMode.MOUSE_MOVE, 'feature_move')
        self.cursorMode.defineEvent(self.clearCursor,
            CursorMode.MOUSE_LEAVE, 'feature_move')

    def clearCursor(self, e=None):
        if self._cursor is None:
            return

        self._cursor.scene().removeItem(self._cursor)
        self._cursor = None

    def featureNew(self, e):
        it = self.window.imageTabCurrent()
        if it is None:
            return

        if self._cursor is None:
            self._cursor = FeatureMarker()
            self._cursor.penNormal.setColor(
                self.window.styles.newFeatureColour)

            it.imView.addGraphicsItem(self._cursor)

        x, y = it.imView.mouseSceneCoords(
            e.x() - self._cursor.width / 2,
            e.y() - self._cursor.height / 2
        )
        self._cursor.setPos(x, y)

    def featureMove(self, e):
        it = self.window.imageTabCurrent()
        if it is None:
            return

        if self._cursor is None:
            self._cursor = FeatureMarker()
            self._cursor.penNormal.setColor(
                self.window.styles.moveFeatureColour)

            it.imView.addGraphicsItem(self._cursor)

        x, y = it.imView.mouseSceneCoords(
            e.x() - self._cursor.width / 2,
            e.y() - self._cursor.height / 2
        )
        self._cursor.setPos(x, y)
