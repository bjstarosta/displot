# -*- coding: utf-8 -*-
from PyQt5 import QtCore


class RegionModel(QtCore.QAbstractTableModel):
    """Data model for the dislocation list.

    Used to prepare and display data within the QTableView it is attached to.
    Note that this class accepts a list of objects (ImageTabRegion like) as its
    data input. Note that even though lists and objects are mutable in Python,
    it's not guaranteed that data changes imposed on the model will be reflected
    on the data list originally passed to the model. Changes to individual objects
    generally will be, while additions of new objects will not without explicit
    handling.

    See http://doc.qt.io/qt-5/qabstractitemmodel.html for a detailed description
    of reimplemented functions.

    Attributes:
        modelData (list): The data model contained within the
            ImageTabList table.
        modelIndices (list): List of string values describing each individual row.
            At present it's just a integer based ID.

    """

    def __init__(self, input=[], parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.headers = ['Pos:X', 'Pos:Y', 'c', 'v', 's']
        self._addQueue = []
        self.setDataList(input)

    def setDataList(self, data):
        self.beginResetModel()
        self.modelData = data
        self.modelIndices = list(map(str, range(1, len(self.modelData) + 1)))
        self.endResetModel()

    def getDataObject(self, row):
        """Returns the ImageTabRegion object corresponding to the specified row.

        Args:
            row (int): Number of the row in the table.

        Returns:
            ImageTabRegion: The region object corresponding to the specified row.

        """
        if row >= len(self.modelData):
            return None
        return self.modelData[row]

    def getDataObjectRow(self, obj):
        """Tries to return the row corresponding to the passed ImageTabRegion
        object.

        Args:
            obj (:obj:`ImageTabRegion`): ImageTabRegion object to compare.

        Returns:
            int: An integer describing the row offset.

        """
        try:
            return self.modelData.index(obj)
        except ValueError:
            return None

    def getCheckedDataObjects(self):
        """Returns all of the ImageTabRegion data objects that have their
        checkbox marked by the user.

        Returns:
            list: A list of ImageTabRegion objects.

        """
        ret = []
        for obj in self.modelData:
            if obj.isSelected == False:
                continue
            ret.append(obj)
        return ret

    def addDataObject(self, obj):
        """Adds an ImageTabRegion objects to the addition queue for the table view.

        Note: Nothing will be added until the insertRows method is called
        specifying the exact offset in the table view to which these objects
        should be added as new rows.

        Args:
            obj (:obj:`ImageTabRegion`): ImageTabRegion object to add.

        """
        self._addQueue.append(obj)

    def notifyDataChanged(self, row):
        """A helper object that emits the dataChanged trigger with the correct
        indices despite only specifying a row number.

        """
        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, 4),
            []
        )

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.modelData)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        elif orientation == QtCore.Qt.Vertical:
            return self.modelIndices[section]

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return QtCore.QVariant(self.modelData[index.row()].midpoint[0])
            if index.column() == 1:
                return QtCore.QVariant(self.modelData[index.row()].midpoint[1])
            if index.column() == 2:
                return QtCore.QVariant(self.modelData[index.row()].cluster_id)

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 2:
                return self.modelData[index.row()].currentPen
            if index.column() == 3:
                if self.modelData[index.row()].isHidden == True:
                    return True
                else:
                    return False

        if role == QtCore.Qt.CheckStateRole:
            if index.column() == 4:
                if self.modelData[index.row()].isSelected == True:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

        return QtCore.QVariant()

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        if role == QtCore.Qt.EditRole:
            if index.column() < 2:
                try:
                    value = int(value)
                except ValueError:
                    return False

            if index.column() == 0:
                self.modelData[index.row()].moveMidpoint(x=value)
                self.modelData[index.row()].updateUiPos()
            if index.column() == 1:
                self.modelData[index.row()].moveMidpoint(y=value)
                self.modelData[index.row()].updateUiPos()
            if index.column() == 2:
                self.modelData[index.row()].cluster_id = value

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 2:
                self.modelData[index.row()].setPen(value)
            if index.column() == 3:
                if value == True:
                    self.modelData[index.row()].isHidden = True
                else:
                    self.modelData[index.row()].isHidden = False

        if role == QtCore.Qt.CheckStateRole:
            if index.column() == 4:
                if value == QtCore.Qt.Checked:
                    self.modelData[index.row()].isSelected = True
                else:
                    self.modelData[index.row()].isSelected = False

        self.dataChanged.emit(index, index, [role])
        return super().setData(index, value, role)

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        if count != len(self._addQueue):
            return False

        row_last = row + count - 1
        row_nextindex = len(self.modelIndices) + 1

        self.beginInsertRows(parent, row, row_last)
        self.modelData[row:row] = self._addQueue
        self.modelIndices[row:row] = list(map(str, range(row_nextindex, row_nextindex + count)))
        self._addQueue = []
        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        row_last = row + count

        self.beginRemoveRows(parent, row, row_last)
        del self.modelData[row:row_last]
        del self.modelIndices[row:row_last]
        self.endRemoveRows()
        return True

    def flags(self, index):
        if index.column() == 3:
            return QtCore.Qt.ItemIsEnabled
        if index.column() == 4:
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEditable | super().flags(index)
