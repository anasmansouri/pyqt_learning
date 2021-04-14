from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from window.window import MyWindow

app = QApplication(sys.argv)
my_window  = MyWindow()
my_window.show()
sys.exit(app.exec_())


