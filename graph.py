
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, QDesktopWidget,
    QSplitter, QStyleFactory, QApplication, QLabel, QGridLayout, QVBoxLayout, QPushButton, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt

class SecondWindow(QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, Qt.Window)
        self.day = 0
        self.build()

    def nextDay(self):
        self.day += 1
        #self.build() ?????

    def build(self):



        numberDay = QLabel(str(self.day))
        hbox1 = QHBoxLayout()
        hbox1.addWidget(numberDay)

        dayData = QLabel("много текста")

        hbox2 = QHBoxLayout()
        hbox2.addWidget(dayData)

        allData = QLabel("много текста")
        hbox3 = QHBoxLayout()
        hbox3.addWidget(allData)

        self.beginButton = QPushButton("Следующий день")
        self.beginButton.clicked.connect(self.nextDay)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.beginButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)


        self.setLayout(vbox)
        e = QApplication.desktop()
        self.setGeometry(0, 0, e.height(), e.width())
        self.setWindowTitle('QSplitter')

        self.center()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class BeginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.secondWin = None
        self.build()

    def openWin(self):
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        print(self.shops.text())
        print(self.full.text())
        self.close()
        self.secondWin.show()

    def build(self):
        shopsTitle = QLabel("Количество магазинов")
        self.shops = QLineEdit()
        fullTitle = QLabel("Количество ...")
        self.full = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addWidget(shopsTitle)
        hbox.addWidget(self.shops)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(fullTitle)
        hbox2.addWidget(self.full)

        self.beginButton = QPushButton("Begin")
        self.beginButton.clicked.connect(self.openWin)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.beginButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)


        self.setGeometry(444, 300, 350, 300)
        self.center()
        self.setWindowTitle('Начальное окно')
        self.show()

        return

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

