import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QStandardItem


class MyTreeModel(QtGui.QStandardItemModel):
    def __init__(self):
        super(MyTreeModel, self).__init__()
        self.parent_item = self.invisibleRootItem()

    def build_tree(self, services_dict):
        for key in services_dict.keys():
            sub_root_item = QStandardItem(str(key))
            self.parent_item.appendRow(sub_root_item)
            for value in services_dict[key]:
                sub_root_item.appendRow(QStandardItem(str(value)))

    def is_not_parent(self, index):
        return index.parent().isValid()
