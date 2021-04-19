
from tree_model import CustomModel
from PyQt5 import QtCore, QtGui, QtWidgets
import json


class MyTreeView(QtWidgets.QTreeView):
    def __init__(self, x):
        super(MyTreeView, self).__init__(x)
        self.tree_model = CustomModel()
        self.setModel(self.tree_model)
        self.setHeaderHidden(True)

    def load_data(self):
        with open('services.json', 'r') as services_json:
            services_dict = json.load(services_json)
            self.tree_model.build_tree(services_dict)
