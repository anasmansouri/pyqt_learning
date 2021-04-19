"""
Reworked code based on
http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
Adapted to Qt5 and fixed column/row bug.
TODO: handle changing data.
"""

import sys
from PyQt5 import QtCore, QtWidgets


class CustomNode(object):
    def __init__(self, data):
        self._data = data
        if type(data) == tuple:
            self._data = list(data)
        if type(data) is str or not hasattr(data, '__getitem__'):
            self._data = [data]

        self._columncount = len(self._data)
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if 0 <= column < len(self._data):
            return self._data[column]

    def columnCount(self):
        return self._columncount

    def childCount(self):
        return len(self._children)

    def child(self, row):
        if 0 <= row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)
        self._columncount = max(child.columnCount(), self._columncount)


class CustomModel(QtCore.QAbstractItemModel):
    def __init__(self, nodes):
        QtCore.QAbstractItemModel.__init__(self)
        self._root = CustomNode(None)
        for node in nodes:
            self._root.addChild(node)

    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, node, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        parent.addChild(node)

    def index(self, row, column, _parent=None):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QtCore.QModelIndex()

        child = parent.child(row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, index):
        if index.isValid():
            return index.internalPointer().columnCount()
        return self._root.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(index.column())
        return None


class MyTreeView:
    """
    """

    def __init__(self):
        self.items = []
        services_top_class = {'Upload Download Management': [
            'Request Download', 'Request Upload'],
            'Stored Data Transmission': ['Clear Diagnostic Informaiton', 'Clear/Reset Emission-Related Diagnostic '
                                                                         'Information'],
            'Diagnostic and Communication Management': ['Link Control', 'Diagnostic session Control'],

            'Remote Activation Of Routine': ['Routine Control / Start Basic Setting',
                                             'Routine Control / Request Routine Results / Basic Setting'],
            'Input Output Control': ['Input Output Control By Identifier / Actuator Test / Short Term '
                                     'Adjustment',
                                     'Input Output Control By Identifier / Actuator Test / Return '
                                     'Control To ECU',
                                     ],
            'Data Transmisson': ['Read Data By Identifier / Measurement Value',
                                 'Read Data By Identfier / Ecu Identification',
                                 ]
        }
        for key in services_top_class.keys():
            self.items.append(CustomNode(key))
            for value in services_top_class[key]:
                self.items[-1].addChild(CustomNode(value))

        self.tw = QtWidgets.QTreeView()
        self.tw.setModel(CustomModel(self.items))
        self.tw.setHeaderHidden(True)

    def add_data(self, data):
        """
        TODO: how to insert data, and update tree.
        """
        # self.items[-1].addChild(CustomNode(['1', '2', '3']))
        # self.tw.setModel(CustomModel(self.items))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mytree = MyTreeView()
    mytree.tw.show()
    sys.exit(app.exec_())
