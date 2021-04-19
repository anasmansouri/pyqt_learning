import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

from mainwindow import Ui_MainWindow
from managementOfServices import ManagementOfServices


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.management_of_services = ManagementOfServices()
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
        elif (event.type() == QtCore.Qt.LeftButton) and source is self.tree_view:
            # self.tree_view.expandToDepth()
            for ix in self.tree_view.selectedIndexes():
                text = ix.data(Qt.DisplayRole)  # or ix.data()
                response = self.management_of_services.fill_infos(text)
                print('{} : {}'.format(text, response))
            # menu = QtWidgets.QMenu()
            # delete_all_action = menu.addAction('delete all')
            # action = menu.exec_(QtGui.QCursor.pos())
            # if action == delete_all_action:
            #     self.delete_the_tree()
        return super(MainWindow, self).eventFilter(source, event)
    #
    # def delete_the_tree(self):
    #     self.tree_model.build_tree(services_dict=[])
    #     self.tree_model.layoutChanged.emit()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
