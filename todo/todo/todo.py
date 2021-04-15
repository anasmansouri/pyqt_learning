import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from models import TodoModel
qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)
        self.addButton.pressed.connect(self.add)
        self.todoView.installEventFilter(self)

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
        return super(MainWindow, self).eventFilter(source, event)

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

    def save(self):
        with open('data.db', 'w') as f:
            json.dump(self.model.todos, f)

    def rightMenuShow(self):
        menu = QtWidgets.QMenu(self)
        add_action = menu.addAction("Add")
        complete_action = menu.addAction("Complete")
        action = menu.exec_(QtGui.QCursor.pos())

        if action == add_action:
            print("Add action")

        if action == complete_action:
            print("complete action")


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
