from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QDesktopWidget,
                             QApplication, QLabel, QGridLayout, QVBoxLayout, QPushButton, QLineEdit)

from classes import Model


def groupByProducts(curList, names):
    ansPriceDict = {}
    ansCountDict = {}
    for curName in names:
        ansPriceDict[curName] = 0
        ansCountDict[curName] = 0
    for curElem in curList:
        if curElem.productTitle in ansPriceDict.keys():
            ansPriceDict[curElem.productTitle] += curElem.price * curElem.numberPack
        else:
            ansPriceDict[curElem.productTitle] = curElem.price * curElem.numberPack

        if curElem.productTitle in ansCountDict.keys():
            ansCountDict[curElem.productTitle] += curElem.numberPack
        else:
            ansCountDict[curElem.productTitle] = curElem.numberPack
    return (ansPriceDict, ansCountDict)


def addNewDay(allDict, newDict):
    for productTitle in newDict.keys():
        if productTitle in allDict.keys():
            allDict[productTitle] += newDict[productTitle]
        else:
            allDict[productTitle] = newDict[productTitle]
class EndWindow(QWidget):
    def __init__(self, parent, day, model, daysCount, allDeletedPrice, allDeletedCount, allSoldPrice, allSoldCount):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, Qt.Window)
        self.day = day
        self.model = model
        self.daysCount = daysCount
        self.allDeletedPrice = allDeletedPrice
        self.allDeletedCount = allDeletedCount
        self.allSoldPrice = allSoldPrice
        self.allSoldCount = allSoldCount
        self.build()

    def build(self):

        grid = QGridLayout()

        numberLine = 0

        curDayTitle = QLabel("Итоговая статистика")
        grid.addWidget(curDayTitle, numberLine, 0)

        endButton = QPushButton("Завершить работу")
        endButton.clicked.connect(self.end)
        grid.addWidget(endButton, numberLine, 3)

        numberLine += 1

        titleTitle = QLabel("Название ")
        grid.addWidget(titleTitle, numberLine, 0)

        soldTitle = QLabel("Продано ")
        grid.addWidget(soldTitle, numberLine, 1)

        deletedTitle = QLabel("Списано ")
        grid.addWidget(deletedTitle, numberLine, 3, 1, 2)

        numberLine += 1

        priceTitle = QLabel("Цена ")
        grid.addWidget(priceTitle, numberLine, 1)

        countTitle = QLabel("Количество ")
        grid.addWidget(countTitle, numberLine, 2)

        priceTitle = QLabel("Цена ")
        grid.addWidget(priceTitle, numberLine, 3)

        countTitle = QLabel("Количество ")
        grid.addWidget(countTitle, numberLine, 4)

        numberLine += 1

        for curProductTitle in self.allDeletedCount.keys():
            curTitle = QLabel(curProductTitle)
            grid.addWidget(curTitle, numberLine, 0)

            curSoldPriceTitle = QLabel(str(self.allSoldPrice[curProductTitle]))
            grid.addWidget(curSoldPriceTitle, numberLine, 1)

            curSoldCountTitle = QLabel(str(self.allSoldCount[curProductTitle]))
            grid.addWidget(curSoldCountTitle, numberLine, 2)

            curDeletedPriceTitle = QLabel(str(self.allDeletedPrice[curProductTitle]))
            grid.addWidget(curDeletedPriceTitle, numberLine, 3)

            curDeletedCountTitle = QLabel(str(self.allDeletedCount[curProductTitle]))
            grid.addWidget(curDeletedCountTitle, numberLine, 4)

            numberLine += 1

        self.setLayout(grid)
        e = QApplication.desktop()
        # self.setGeometry(0, 0, e.height(), e.width())
        self.setGeometry(444, 300, 800, 900)
        self.setWindowTitle('Итог')

        self.center()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def end(self):
        self.close()


class DayWindow(QWidget):
    def __init__(self, parent, day, model, daysCount, allDeletedPrice, allDeletedCount, allSoldPrice, allSoldCount):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, Qt.Window)
        self.day = day
        self.model = model
        self.daysCount = daysCount
        self.allDeletedPrice = allDeletedPrice
        self.allDeletedCount = allDeletedCount
        self.allSoldPrice = allSoldPrice
        self.allSoldCount = allSoldCount
        self.build()

    def nextDay(self):
        nextDayModel = self.model.nextDay()
        if self.day != self.daysCount:
            dayWin = DayWindow(self, self.day + 1, nextDayModel, self.daysCount, self.allDeletedPrice,
                                     self.allDeletedCount, self.allSoldPrice, self.allSoldCount)
            self.close()
            dayWin.show()
        else:
            endWin = EndWindow(self, self.day, self.model, self.daysCount, self.allDeletedPrice,
                                     self.allDeletedCount, self.allSoldPrice, self.allSoldCount)
            self.close()
            endWin.show()
            return

    def build(self):

        grid = QGridLayout()
        (dayMoney, deleted, sold, names) = self.model.getInfo()
        (curDeletedPrice, curDeletedCount) = groupByProducts(deleted[-1], names)
        (curSoldPrice, curSoldCount) = groupByProducts(sold[-1], names)
        addNewDay(self.allDeletedPrice, curDeletedPrice)
        addNewDay(self.allDeletedCount, curDeletedCount)
        addNewDay(self.allSoldPrice, curSoldPrice)
        addNewDay(self.allSoldCount, curSoldCount)


        numberDay = QLabel("День " + str(self.day))
        grid.addWidget(numberDay, 0, 0)

        beginButton = QPushButton("Следующий день")
        beginButton.clicked.connect(self.nextDay)

        grid.addWidget(beginButton, 0, 2)

        curDayTitle = QLabel("Статистика текущего дня")
        grid.addWidget(curDayTitle, 1, 0)

        # считаем все в розничных упаковках, тк оптовые - меняяются

        titleTitle = QLabel("Название ")
        grid.addWidget(titleTitle, 2, 0)

        soldTitle = QLabel("Продано ")
        grid.addWidget(soldTitle, 2, 1)

        deletedTitle = QLabel("Списано ")
        grid.addWidget(deletedTitle, 2, 3, 1, 2)

        priceTitle = QLabel("Цена ")
        grid.addWidget(priceTitle, 3, 1)

        countTitle = QLabel("Количество ")
        grid.addWidget(countTitle, 3, 2)

        priceTitle = QLabel("Цена ")
        grid.addWidget(priceTitle, 3, 3)

        countTitle = QLabel("Количество ")
        grid.addWidget(countTitle, 3, 4)

        numberLine = 4
        for curProductTitle in names:
            curTitle = QLabel(curProductTitle)
            grid.addWidget(curTitle, numberLine, 0)

            curSoldPriceTitle = QLabel(str(curSoldPrice[curProductTitle]))
            grid.addWidget(curSoldPriceTitle, numberLine, 1)

            curSoldCountTitle = QLabel(str(curSoldCount[curProductTitle]))
            grid.addWidget(curSoldCountTitle, numberLine, 2)

            curDeletedPriceTitle = QLabel(str(curDeletedPrice[curProductTitle]))
            grid.addWidget(curDeletedPriceTitle, numberLine, 3)

            curDeletedCountTitle = QLabel(str(curDeletedCount[curProductTitle]))
            grid.addWidget(curDeletedCountTitle, numberLine, 4)

            numberLine += 1



        curDayTitle = QLabel("Итоговая статистика")
        grid.addWidget(curDayTitle, numberLine, 0)
        numberLine += 1

        titleTitle = QLabel("Название ")
        grid.addWidget(titleTitle, numberLine, 0)

        soldTitle = QLabel("Продано ")
        grid.addWidget(soldTitle, numberLine, 1)

        deletedTitle = QLabel("Списано ")
        grid.addWidget(deletedTitle, numberLine, 3, 1, 2)

        numberLine += 1
        
        priceTitle = QLabel("Цена ")
        grid.addWidget(priceTitle, numberLine, 1)

        countTitle = QLabel("Количество ")
        grid.addWidget(countTitle, numberLine, 2)

        priceTitle = QLabel("Цена ")
        grid.addWidget(priceTitle, numberLine, 3)

        countTitle = QLabel("Количество ")
        grid.addWidget(countTitle, numberLine, 4)

        numberLine += 1

        for curProductTitle in names:
            curTitle = QLabel(curProductTitle)
            grid.addWidget(curTitle, numberLine, 0)

            curSoldPriceTitle = QLabel(str(self.allSoldPrice[curProductTitle]))
            grid.addWidget(curSoldPriceTitle, numberLine, 1)

            curSoldCountTitle = QLabel(str(self.allSoldCount[curProductTitle]))
            grid.addWidget(curSoldCountTitle, numberLine, 2)

            curDeletedPriceTitle = QLabel(str(self.allDeletedPrice[curProductTitle]))
            grid.addWidget(curDeletedPriceTitle, numberLine, 3)

            curDeletedCountTitle = QLabel(str(self.allDeletedCount[curProductTitle]))
            grid.addWidget(curDeletedCountTitle, numberLine, 4)

            numberLine += 1

        self.setLayout(grid)
        e = QApplication.desktop()
        # self.setGeometry(0, 0, e.height(), e.width())
        self.setGeometry(444, 300, 800, 900)
        self.setWindowTitle('Текущий день')

        self.center()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class BeginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build()

    def openWin(self):
        model = Model(int(self.products.text()), int(self.shops.text()))
        dayWin = DayWindow(self, 1, model.nextDay(), int(self.daysCount.text()), {},
                                 {}, {}, {})
        self.close()
        dayWin.show()

    def build(self):
        productsTitle = QLabel("Количество продуктов")
        self.products = QLineEdit()
        shopsTitle = QLabel("Количество магазинов")
        self.shops = QLineEdit()
        daysCountTitle = QLabel("Количество дней")
        self.daysCount = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addWidget(productsTitle)
        hbox.addWidget(self.products)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(shopsTitle)
        hbox2.addWidget(self.shops)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(daysCountTitle)
        hbox3.addWidget(self.daysCount)

        self.beginButton = QPushButton("Begin")
        self.beginButton.clicked.connect(self.openWin)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.beginButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

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
