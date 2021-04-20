import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

tick = QtGui.QImage('tick.png')


class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, services=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.services = services or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.services[index.row()]

            return text

        if role == Qt.DecorationRole:
            status, _ = self.services[index.row()]

            if status:
                return tick

    def rowCount(self, index):
        return len(self.services)


