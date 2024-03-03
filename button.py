# This script is not ready yet, the purpose is to build a simple window application to trigger voice capture 

import sys
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(1200, 300, 500, 500)
    win.setWindowTitle("click here")
    # win.setWindowIcon()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()
    