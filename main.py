from graph import BeginWindow
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame,
    QSplitter, QStyleFactory, QApplication, QLabel, QGridLayout, QVBoxLayout, QPushButton, QInputDialog)
from PyQt5.QtCore import Qt

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = BeginWindow()
    sys.exit(app.exec_())