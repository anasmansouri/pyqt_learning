from PyQt5 import QtCore, QtGui, QtWidgets
import json

from PyQt5.QtCore import QModelIndex

from my_tree_model import MyTreeModel


class MyTreeView(QtWidgets.QTreeView):
    def __init__(self, x):
        super(MyTreeView, self).__init__(x)
        self.tree_model = MyTreeModel()
        self.setModel(self.tree_model)
        self.setHeaderHidden(True)
        # self.expanded.connect(self.chihaja)

    def load_data(self):
        with open('services.json', 'r') as services_json:
            services_dict = json.load(services_json)
            self.tree_model.build_tree(services_dict)

    # def chihaja(self, index):
    #     item = self.tree_model.itemFromIndex(index)
    #     print(item.text())



