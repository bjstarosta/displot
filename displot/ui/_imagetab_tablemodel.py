# -*- coding: utf-8 -*-
"""displot - Image tab table view data model definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtCore
from displot.io import DisplotData


class ImageTabTableModel(QtCore.QAbstractTableModel, DisplotData):
    """Feature table data model.

    Used to prepare and display data within the QTableView it is attached to.
    This class functions independently from the internal data store that is
    operated on by the program, and as such must be synced using the relevant
    methods in ui.ImageTab to pass the data back and forth from the internal
    data store.

    See http://doc.qt.io/qt-5/qabstractitemmodel.html for a detailed
    description of reimplemented functions.

    Attributes:
        headers (list): List of descriptions present in the header row.
        modelData (list): The data contained within the model.

    """

    POS_FORMAT = 'X:{0}, Y:{1}'
    CONF_FORMAT = '{:.3f}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers = ['', '', 'Position', 'Confidence']
        self._addQueue = []
        self.setModelData([])

    def setModelData(self, data):
        """Pass a list of feature objects to the model.

        Data indices are set as integers corresponding to the object index
        in the list.

        Args:
            data (list): List of feature objects.

        Returns:
            None

        """
        self.beginResetModel()
        self.modelData = data
        self.endResetModel()

    def getModelData(self):
        """Return current list of feature objects.

        Returns:
            list: List of feature objects.

        """
        return self.modelData

    def getDataObject(self, row):
        """Returns the feature object corresponding to the specified row.

        Args:
            row (int): Number of the row in the table.

        Returns:
            ImageTabFeature: Feature object.
                Or None if the row index is out of bounds.

        """
        if row >= len(self.modelData) or row < 0:
            return None
        return self.modelData[row]

    def getDataObjectRow(self, obj):
        """Get table row associated with the passed feature object.

        Args:
            obj (ImageTabFeature): Feature object.

        Returns:
            int: An integer describing the row offset.
                Or None if no associated row is found.

        """
        try:
            return self.modelData.index(obj)
        except ValueError:
            return None

    def getSelectedObjects(self):
        """Return feature objects that have their table row checkbox checked.

        Returns:
            list: List of feature objects.

        """
        ret = []
        for obj in self.modelData:
            if obj.isSelected is True:
                ret.append(obj)
        return ret

    def addDataObject(self, obj):
        """Add a feature object to the queue for the table view.

        Note: Nothing will be added until the insertRows method is called
        specifying the exact offset in the table view to which these objects
        should be added as new rows.

        Args:
            obj (ImageTabFeature): Object to add.

        Returns:
            None

        """
        self._addQueue.append(obj)

    def notifyRowChanged(self, row):
        """Emit dataChanged signal while translating row number to cell indices.

        Args:
            row (int): Row number.

        Returns:
            None

        """
        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, self.columnCount()),
            []
        )

    def notifyAllChanged(self):
        """Emit dataChanged signal for entire model.

        Returns:
            None

        """
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()),
            []
        )

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Return the number of rows under the given parent.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            parent (QtCore.QModelIndex): Parent element.

        Returns:
            int: Row count.

        """
        return len(self.modelData)

    def columnCount(self, parent=QtCore.QModelIndex()):
        """Return the number of columns under the given parent.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            parent (QtCore.QModelIndex): Parent element.

        Returns:
            int: Column count.

        """
        return len(self.headers)

    def headerData(self, section, orientation, role):
        """Return the data for the given role and section in the header.

        Determines what is displayed in the header rows/columns.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            section (int): For horizontal headers, the section number
                corresponds to the column number. Similarly, for vertical
                headers, the section number corresponds to the row number.
            orientation (QtCore.Qt.Orientation): See Qt::Orientation.
            role (int): See Qt::ItemDataRole.

        Returns:
            QtCore.QVariant: Header data object.

        """
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]

    def data(self, index, role):
        """Return the data stored under the given role for the index.

        Determines how model data is applied to the table UI.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            index (QtCore.QModelIndex): Cell index.
            role (int): See Qt::ItemDataRole.

        Returns:
            QtCore.QVariant: Cell data object.

        """
        if not index.isValid():
            return QtCore.QVariant()

        obj = self.modelData[index.row()]

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 2:
                return QtCore.QVariant(self.POS_FORMAT.format(obj.x, obj.y))
            if index.column() == 3:
                return QtCore.QVariant(self.CONF_FORMAT.format(obj.confidence))
            """if index.column() == 2:
                return QtCore.QVariant(obj.cluster_id)"""

        if role == QtCore.Qt.DecorationRole:
            """if index.column() == 2:
                return obj.currentPen"""
            if index.column() == 1:
                if obj.isHidden is True:
                    return True
                else:
                    return False

        if role == QtCore.Qt.CheckStateRole:
            if index.column() == 0:
                if obj.isSelected is True:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

        return QtCore.QVariant()

    def setData(self, index, value, role):
        """Sets the role data for the item at index to value.

        Determines how changes to data in the table UI apply to the model data.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            index (QtCore.QModelIndex): Cell index.
            value (QtCore.QVariant): Data object to place in the cell.
            role (int): See Qt::ItemDataRole.

        Returns:
            bool: Returns True if successful; otherwise returns False.

        """
        if not index.isValid():
            return False

        obj = self.modelData[index.row()]

        """if role == QtCore.Qt.EditRole:
            if index.column() < 2:
                try:
                    value = int(value)
                except ValueError:
                    return False

            if index.column() == 0:
                obj.x = value
            if index.column() == 1:
                obj.y = value
            if index.column() == 2:
                obj.cluster_id = value

            obj.update()"""

        if role == QtCore.Qt.DecorationRole:
            """if index.column() == 2:
                obj.setPen(value)"""
            if index.column() == 1:
                if value is True:
                    obj.isHidden = True
                else:
                    obj.isHidden = False

        if role == QtCore.Qt.CheckStateRole:
            if index.column() == 0:
                if value == QtCore.Qt.Checked:
                    obj.select(True)
                else:
                    obj.select(False)

        self.dataChanged.emit(index, index, [role])
        return super().setData(index, value, role)

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        """Inserts count rows into the model before the given row.

        Items in the new row will be children of the item represented by the
        parent model index.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            row (int): Row index before which to perform the insertion.
            count (int): Number of rows to insert.
            parent (QtCore.QModelIndex): Parent element.
                Items in the new rows will be children of the item represented
                by the parent model index.

        Returns:
            bool: Returns True if successful; otherwise returns False.

        """
        if count != len(self._addQueue):
            return False

        row_last = row + count - 1

        self.beginInsertRows(parent, row, row_last)
        self.modelData[row:row] = self._addQueue
        self._addQueue = []
        self.endInsertRows()

        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        """Remove count rows starting with the given row from the model.

        Note: If you only want to remove a single row, the count parameter
        should be set to 0.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            row (int): Row index at which to begin the deletion.
            count (int): Number of rows to delete.
            parent (QtCore.QModelIndex): Parent element.

        Returns:
            bool: Returns True if successful; otherwise returns False.

        """
        row_last = row + count

        self.beginRemoveRows(parent, row, row_last)
        del self.modelData[row:row_last + 1]
        self.endRemoveRows()

        return True

    def flags(self, index):
        """Return the item flags for the given index.

        Reimplemented from QtCore.QAbstractItemModel as required.
        See: https://doc.qt.io/qt-5/qabstractitemmodel.html

        Args:
            index (QtCore.QModelIndex): Cell index.

        Returns:
            QtCore.Qt.ItemFlags: Flags corresponding to a given cell.

        """
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled
        if index.column() == 0:
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEditable | super().flags(index)
