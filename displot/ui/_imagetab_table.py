# -*- coding: utf-8 -*-
"""displot - Image tab table view UI functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class ImageTabTable(QtWidgets.QTableView):
    """Image tab table view object.

    Attributes:
        itab (ui.ImageTab): Parent image tab object of this table.
            Must be set after layout has been constructed.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itab = None

    def selectedItem(self):
        """Returns exactly one selected feature object.

        Note that this follows cell highlight selection, not checkbox
        selection.

        Returns:
            ui.ImageTabFeature: Feature object corresponding to the selected
                row, or None if no object is selected.

        """
        ind = self.selectedIndexes()
        model = self.model()
        if len(ind) > 0:
            return model.getDataObject(ind[0].row())
        return None

    def selectionChanged(self, selected, deselected):
        if self.itab is not None:
            sel = self.selectedItem()
            if (sel is not None
            and self.itab.layout.button_AutoCenterFrags.isChecked() is True):
                sel.centerOn()

        super().selectionChanged(selected, deselected)

    """def mousePressEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            index = self.indexAt(e.pos())
            if index.column() == 2:
                self.edit(index)
        super().mousePressEvent(e)"""


class FeatureColour(QtWidgets.QItemDelegate):

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

        # pen = index.data(QtCore.Qt.DecorationRole)
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
        if editor is None:
            return super().setEditorData(editor, index)

        # currentPen = index.data(QtCore.Qt.DecorationRole)
        # boxIndex = self._featureStyle.userPens.index(currentPen)
        boxIndex = index.data(QtCore.Qt.DisplayRole)
        if boxIndex >= 0:
            editor.setCurrentIndex(boxIndex)

    def setModelData(self, editor, model, index):
        if editor is None:
            return super().setEditorData(editor, model, index)

        newPen = self._featureStyle.userPens[editor.currentIndex()]
        model.setData(index, newPen, QtCore.Qt.DecorationRole)
        model.setData(index, editor.currentIndex(), QtCore.Qt.EditRole)

    def commitAndSaveData(self):
        self.commitData.emit(self._cb)
        self.closeEditor.emit(self._cb)


class FeatureVisibility(QtWidgets.QItemDelegate):
    """Delegate class for the individual item visibility checkbox.

    See http://doc.qt.io/qt-5/qitemdelegate.html for a detailed description
    of reimplemented functions.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap(":/feathericons/3rdparty/feather/icons/eye-off.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On
        )
        self.icon.addPixmap(
            QtGui.QPixmap(":/feathericons/3rdparty/feather/icons/eye.svg"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.iconSize = 14

    def paint(self, painter, option, index):
        painter.save()

        if index.data(QtCore.Qt.DecorationRole) is True:
            state = QtGui.QIcon.On
        else:
            state = QtGui.QIcon.Off

        pixmap = self.icon.pixmap(self.iconSize, self.iconSize,
            QtGui.QIcon.Normal, state)
        xy = (
            option.rect.x() + (option.rect.width() / 2) - (self.iconSize / 2),
            option.rect.y() + (option.rect.height() / 2) - (self.iconSize / 2)
        )
        painter.drawPixmap(xy[0], xy[1], pixmap)
        super().drawFocus(painter, option, option.rect)

        painter.restore()
        super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if index.data(QtCore.Qt.DecorationRole) is True:
            state = False
        else:
            state = True

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            return model.setData(index, state, QtCore.Qt.DecorationRole)
        else:
            return False


class FeatureCheckBox(QtWidgets.QItemDelegate):
    """Delegate class for the persistent checkbox selection.

    See http://doc.qt.io/qt-5/qitemdelegate.html for a detailed description
    of reimplemented functions.

    """

    def paint(self, painter, option, index):
        # if index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
        #     state = QtCore.Qt.Checked
        # else:
        #     state = QtCore.Qt.Unchecked

        # super().drawCheck(painter, option, option.rect, state)
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
