from graph import BeginWindow
import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QVBoxLayout, QPushButton, QInputDialog)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = BeginWindow(first_flag = True)
    sys.exit(app.exec_())