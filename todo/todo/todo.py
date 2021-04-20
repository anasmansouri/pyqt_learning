import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import json
from mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setupTreeView()
        self.setupListView()
        self.setupEvents()

    def setupTreeView(self):
        self.tree_view.load_data()

    def setupListView(self):
        self.todoView.load_data()

    def setupEvents(self):
        self.addButton.pressed.connect(lambda: self.todoView.add(self.todoEdit.text()))
        self.todoView.installEventFilter(self)
        self.tree_view.installEventFilter(self)
        self.tree_view.clicked.connect(self.tree_item_clicked)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu) and source is self.todoView:
            menu = QtWidgets.QMenu()
            delete_action = menu.addAction('delete')
            complete_action = menu.addAction('complete')
            action = menu.exec_(QtGui.QCursor.pos())

            if action == complete_action:
                self.todoView.complete()
            elif action == delete_action:
                self.todoView.delete()
            return True
        return super(MainWindow, self).eventFilter(source, event)

    def tree_item_clicked(self, index):
        if self.tree_view.tree_model.is_not_parent(index):
            child = self.tree_view.tree_model.itemFromIndex(index).text()
            parent = self.tree_view.tree_model.itemFromIndex(index.parent()).text()
            parent_and_child = [parent, child]
            print(parent_and_child)
            # self.todoView.list_model.services = self.tree_view.tree_model.
            # with open('services.json', 'r') as services_json:
            #     services_dict = json.load(services_json)
            #     print(services_dict[parent][child])


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
