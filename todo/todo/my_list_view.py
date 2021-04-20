from PyQt5 import QtCore, QtGui, QtWidgets
import json
from list_model import TodoModel


class MyListView(QtWidgets.QListView):
    def __init__(self, x):
        super(MyListView, self).__init__(x)
        self.list_model = TodoModel()
        self.setModel(self.list_model)

    def set_dids(self, dids=None):
        if dids is not None:
            self.list_model.services = dids
            self.list_model.layoutChanged().emit()

    def add(self, text):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """

        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.list_model.services.append((False, text))
            # Trigger refresh.
            self.list_model.layoutChanged.emit()
            # Empty the input
            self.save()

    def delete(self):
        indexes = self.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.list_model.services[index.row()]
            self.list_model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.clearSelection()
            self.save()

    def complete(self):
        indexes = self.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.list_model.services[row]
            self.list_model.services[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.list_model.dataChanged.emit(index, index)
            # # Clear the selection (as it is no longer valid).
            self.clearSelection()
            self.save()

    def load_data(self):
        try:
            with open('data.db', 'r') as f:
                self.list_model.services = json.load(f)

        except Exception:
            pass

    def save(self):
        with open('data.db', 'w') as f:
            json.dump(self.list_model.services, f)
