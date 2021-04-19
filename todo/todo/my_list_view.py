from PyQt5 import QtCore, QtGui, QtWidgets
import json


class MyListView(QtWidgets.QListView):
    def __init__(self):
        pass

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
        # try:
        #     with open('data_2.json','r') as f:
        #         self.tree_model.item
