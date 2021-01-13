# -*- coding: utf-8 -*-
"""displot - UI style definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtGui


class GuiStyles(object):
    """UI style definitions in a single, global object.

    Attributes:
        userColours (list): List of QtGui.QColor objects specifying
            selectable colours for dislocation markers.
        userPens (list): List of QtGui.QPen objects defined using userColours.
        userBrushes (list): List of QtGui.QBrush objects defined using
            userColours.
        defaultPen (QtGui.QPen): Default QPen object.
        defaultBrush (QtGui.QBrush): Default QBrush object.
        highlightPen (QtGui.QPen): QPen object for highlighted markers.
        newCursorPen (QtGui.QPen): QPen object for new marker placement cursor.
        moveCursorPen (QtGui.QPen): QPen object for move marker placement
            cursor.

    """

    def __init__(self):

        self.userColours = [
            QtGui.QColor(0xDD0000),
            QtGui.QColor(0xEEEE00),
            QtGui.QColor(0x00CC00),
            QtGui.QColor(0x6666FF),
            QtGui.QColor(0x88BB00),
            QtGui.QColor(0xFFBB00),
            QtGui.QColor(0x00BBFF),
            QtGui.QColor(0x99DD99)
        ]

        self.userPens = []
        self.userBrushes = []
        for c in self.userColours:
            self.userPens.append(QtGui.QPen(c))
            self.userBrushes.append(QtGui.QBrush(c))

        self.defaultPen = self.userPens[len(self.userPens) - 1]
        self.defaultBrush = self.userBrushes[len(self.userBrushes) - 1]

        self.defaultColour = self.userColours[len(self.userColours) - 1]
        self.highlightColour = QtGui.QColor(0xFFFFFF)
        self.newFeatureColour = QtGui.QColor(0xF20884)
        self.moveFeatureColour = QtGui.QColor(0x02ABEA)
