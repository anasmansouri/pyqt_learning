import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from models import TodoModel
from tree_model_v_2 import CustomModel, CustomNode
# qt_creator_file = "mainwindow.ui"
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
from mainwindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = TodoModel()
        self.tree_model = CustomModel()
        self.load()
        self.todoView.setModel(self.model)
        self.load_services()
        self.addButton.pressed.connect(self.add)
        self.todoView.installEventFilter(self)
        self.tree_view.installEventFilter((self))

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu) and source is self.todoView:
            menu = QtWidgets.QMenu()
            delete_action = menu.addAction('delete')
            complete_action = menu.addAction('complete')
            action = menu.exec_(QtGui.QCursor.pos())
            if action == complete_action:
                self.complete()
            elif action == delete_action:
                self.delete()
            return True
        elif (event.type() == QtCore.QEvent.ContextMenu) and source is self.tree_view:
            menu = QtWidgets.QMenu()
            delete_all_action = menu.addAction('delete all')
            action = menu.exec_(QtGui.QCursor.pos())
            if action == delete_all_action:
                self.delete_the_tree()
        return super(MainWindow, self).eventFilter(source, event)

    def delete_the_tree(self):
        self.tree_model.build_tree(services_dict=[])
        self.tree_model.layoutChanged.emit()

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.        
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal 
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open('data.db', 'r') as f:
                self.model.todos = json.load(f)
        except Exception:
            pass
        # try:
        #     with open('data_2.json','r') as f:
        #         self.tree_model.item

    def load_services(self):

        with open('data_2.json', 'r') as services_json:
            services_dict = json.load(services_json)
            self.tree_model = CustomModel()
            self.tree_model.build_tree(services_dict)
            self.tree_view.setModel(self.tree_model)
            self.tree_view.setHeaderHidden(True)

    def save(self):
        with open('data.db', 'w') as f:
            json.dump(self.model.todos, f)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
