import PyQt5.QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QDesktopWidget, QHeaderView, QSlider,
                             QApplication, QLabel, QGridLayout, QVBoxLayout, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem)

from classes import Model

MAX_WIDTH = 0
SOLD_WIDTH = 1
PRICE_WIDTH = 1
COUNT_WIDTH = 1
DELETED_WIDTH = 1
BALANCE_WIDTH = 1
SHOP_WIDTH = 1
REQ_WIDTH = 1
GIVEN_WIDTH = 1
NAMES_WIDTH = 1
DATA_WIDTH = 1
TITLE_WIDTH = 1
LINE_SIZE = 1
COLUMN_SIZE = 1
TITLE_SIZE = 1
END_WINDOW_SIZE = 2
FONT_SIZE = 20


def create_sold_delete_labels(table, number_line, number_column):
    global NAMES_WIDTH, SOLD_WIDTH, DELETED_WIDTH
    table.setItem(number_line, number_column, QTableWidgetItem("Название"))
    number_column += NAMES_WIDTH
    table.setItem(number_line, number_column, QTableWidgetItem("Продано\n(рубли)"))
    number_column += PRICE_WIDTH
    table.setItem(number_line, number_column, QTableWidgetItem("Продано\n(упаковки)"))
    number_column += COUNT_WIDTH
    table.setItem(number_line, number_column, QTableWidgetItem("Списано\n(рубли)"))
    number_column += PRICE_WIDTH
    table.setItem(number_line, number_column, QTableWidgetItem("Списано\n(упаковки)"))
    number_column += COUNT_WIDTH
    return number_column


def fill_column(table, number_first_line, number_column, data, names):
    number_line = number_first_line  # первая, с которой начали
    for name in names:
        if data:
            elem = str(round(data[name]))
        else:
            elem = name  # заполняем столбец названий
        table.setItem(number_line, number_column, QTableWidgetItem(elem))
        number_line += LINE_SIZE


def create_statistics(table, number_line, number_column, names, sold_price, sold_count, deleted_price, deleted_count):
    fill_column(table, number_line, number_column, None, names)
    number_column += COLUMN_SIZE

    fill_column(table, number_line, number_column, sold_price, names)
    number_column += COLUMN_SIZE
    fill_column(table, number_line, number_column, sold_count, names)
    number_column += COLUMN_SIZE
    fill_column(table, number_line, number_column, deleted_price, names)
    number_column += COLUMN_SIZE
    fill_column(table, number_line, number_column, deleted_count, names)
    number_column += COLUMN_SIZE

    number_line += len(names)

    return number_line, number_column


def create_shops_info_labels(table, number_line, number_column, count_shops):
    global SHOP_WIDTH
    for i in range(1, count_shops + TITLE_SIZE):
        table.setItem(number_line, number_column, QTableWidgetItem("Магазин " + str(i) + "\n(Запр.)"))
        number_column += SHOP_WIDTH
        table.setItem(number_line, number_column, QTableWidgetItem("Магазин " + str(i) + "\n(Пред.)"))
        number_column += SHOP_WIDTH
    return number_column


def create_shops_info(table, number_line, number_column, count_shops, names, shops_requests, shops_given):
    for i in range(1, count_shops + TITLE_SIZE):
        fill_column(table, number_line, number_column, shops_requests[i], names)
        number_column += REQ_WIDTH
        fill_column(table, number_line, number_column, shops_given[i], names)
        number_column += GIVEN_WIDTH
    return number_column


def create_data_info(grid, number_line, number_column, data_info):
    global DATA_WIDTH
    s = "Наименований: " + str(data_info[0]) + ", "
    s += "магазинов:" + str(data_info[1]) + ", "
    s += "дней:" + str(data_info[2]) + ", "
    s += "спрос:" + str(data_info[3])
    title = QLabel(s)
    title.setAlignment(Qt.AlignHCenter)
    grid.addWidget(title, number_line, number_column, 1, END_WINDOW_SIZE)


def create_day_table(table, names, cur_sold_price,
                     cur_sold_count, cur_deleted_price,
                     cur_deleted_count, last_shop_requests, last_shop_given, count_shops, balance):
    (number_line, number_column) = (0, 0)
    number_column = create_sold_delete_labels(table, number_line, number_column)
    table.setItem(number_line, number_column, QTableWidgetItem("Осталось\n(упаковки)"))
    number_column += COLUMN_SIZE
    create_shops_info_labels(table, number_line, number_column, count_shops)
    number_line += LINE_SIZE
    number_column = 0
    (new_number_line, number_column) = create_statistics(table, number_line, number_column, names, cur_sold_price,
                                                         cur_sold_count, cur_deleted_price, cur_deleted_count)
    fill_column(table, number_line, number_column, balance, names)
    number_column += COLUMN_SIZE
    create_shops_info(table, number_line, number_column, count_shops, names, last_shop_requests, last_shop_given)
    return


def create_itog_table(table, names, all_sold_price, all_sold_count, all_deleted_price, all_deleted_count, count_shops,
                      all_shop_requests, all_shop_given):
    number_column = 0
    number_line = 0
    number_column = create_sold_delete_labels(table, number_line, number_column)
    create_shops_info_labels(table, number_line, number_column, count_shops)
    number_line += LINE_SIZE
    number_column = 0
    (new_number_line, number_column) = create_statistics(table, number_line, number_column, names, all_sold_price,
                                                         all_sold_count, all_deleted_price, all_deleted_count)
    create_shops_info(table, number_line, number_column, count_shops, names, all_shop_requests, all_shop_given)
    return


def create_finish_table(table, names, all_sold_price, all_sold_count, all_deleted_price, all_deleted_count, balance):
    number_column = 0
    number_line = 0
    number_column = create_sold_delete_labels(table, number_line, number_column)
    table.setItem(number_line, number_column, QTableWidgetItem("Осталось\n(упаковки)"))
    number_line += LINE_SIZE
    number_column = 0
    (new_number_line, new_number_column) = create_statistics(table, number_line, number_column, names, all_sold_price,
                                                             all_sold_count, all_deleted_price, all_deleted_count)
    fill_column(table, number_line, new_number_column, balance, names)
    return


class EndWindow(QWidget):
    def __init__(self, parent, model):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, Qt.Window)
        info = model.get_info()
        (names, all_sold_price, all_sold_count, all_deleted_price, all_deleted_count, balance) = (
            info.names, info.all_sold_price, info.all_sold_count, info.all_deleted_price, info.all_deleted_count,
            info.balance)
        grid = QGridLayout()
        table = QTableWidget(self)
        table.setWordWrap(True)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        global PRICE_WIDTH, COUNT_WIDTH, NAMES_WIDTH, BALANCE_WIDTH
        width = 2 * (PRICE_WIDTH + COUNT_WIDTH) + NAMES_WIDTH + BALANCE_WIDTH
        table.setColumnCount(width)
        count_shops = model.get_count_shops()
        count_products = model.get_count_products()
        table.setRowCount(count_products + TITLE_SIZE)
        number_line = 0
        number_column = 0
        title = QLabel("Итоговая статистика")
        title.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        grid.addWidget(title, number_line, 0, 1, END_WINDOW_SIZE)
        number_line += LINE_SIZE
        data_info = model.get_data_info()
        create_data_info(grid, number_line, number_column, data_info)
        number_line += LINE_SIZE
        (all_sold, all_deleted) = model.get_all_money()
        money_label = QLabel(
            "Продано на " + str(round(all_sold)) + "(руб.), списано на " + str(round(all_deleted)) + "(руб.)")
        money_label.setAlignment(Qt.AlignHCenter)
        grid.addWidget(money_label, number_line, number_column, 1, END_WINDOW_SIZE)
        number_line += LINE_SIZE
        create_finish_table(table, names, all_sold_price, all_sold_count, all_deleted_price, all_deleted_count, balance)
        grid.addWidget(table, number_line, 0, 1, END_WINDOW_SIZE)
        number_line += count_shops + TITLE_SIZE
        end_button = QPushButton("Завершить работу")
        end_button.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        end_button.setStyleSheet('background: red;')
        end_button.clicked.connect(self.end)
        grid.addWidget(end_button, number_line, 0)
        begin_button = QPushButton("Начать  заново  ")
        begin_button.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        begin_button.setStyleSheet('background: green;')
        begin_button.clicked.connect(self.begin_new)
        global MAX_WIDTH
        grid.addWidget(begin_button, number_line, 1)
        self.setLayout(grid)
        QApplication.desktop()
        self.resize(640, 400)
        self.setWindowTitle('Итог')

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def end(self):
        self.close()

    def begin_new(self):
        new_win = BeginWindow(self)
        self.close()
        new_win.show()
        return


class DayWindow(QWidget):
    def __init__(self, parent, model):
        # считаем все в розничных упаковках, тк оптовые - меняяются

        super().__init__(parent, Qt.Window)
        self.model = model
        widget = QWidget()
        grid = QGridLayout(widget)
        info = self.model.get_info()
        (names, cur_sold_price, cur_sold_count, cur_deleted_price, cur_deleted_count, all_sold_price, all_sold_count,
         all_deleted_price, all_deleted_count, balance) = (
        info.names, info.cur_sold_price, info.cur_sold_count, info.cur_deleted_price, info.cur_deleted_count, info.all_sold_price,
        info.all_sold_count, info.all_deleted_price, info.all_deleted_count, info.balance)
        global SHOP_WIDTH, DELETED_WIDTH, SOLD_WIDTH, BALANCE_WIDTH, NAMES_WIDTH, TITLE_WIDTH, MAX_WIDTH
        count_shops = self.model.get_count_shops()
        count_products = self.model.get_count_products()
        (all_shop_requests, last_shop_requests, all_shop_given, last_shop_given) = (
            info.all_shop_requests, info.last_shop_requests, info.all_shop_given, info.last_shop_given)
        number_day = QLabel("День " + str(self.model.get_day_number()))
        number_day.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        number_line = 0
        number_column = 0
        grid.addWidget(number_day, number_line, number_column)
        number_column += TITLE_WIDTH
        data_info = self.model.get_data_info()
        create_data_info(grid, number_line, number_column, data_info)
        number_line += LINE_SIZE
        number_column = 0
        cur_day_title = QLabel("Текущий день")
        cur_day_title.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        grid.addWidget(cur_day_title, number_line, 0)
        number_column += TITLE_WIDTH
        (day_sold, day_deleted) = self.model.get_day_money()
        money_label = QLabel(
            "Продано на " + str(round(day_sold)) + "(руб.), списано на " + str(round(day_deleted)) + "(руб.)")
        grid.addWidget(money_label, number_line, number_column)
        number_line += LINE_SIZE

        table1 = QTableWidget(self)
        table1.setWordWrap(True)
        table1.setColumnCount(MAX_WIDTH)
        table1.setRowCount(count_products + TITLE_SIZE)
        table1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        number_column = 0
        grid.addWidget(table1, number_line, number_column, count_shops, MAX_WIDTH)
        create_day_table(table1, names, cur_sold_price,
                         cur_sold_count, cur_deleted_price,
                         cur_deleted_count, last_shop_requests, last_shop_given, count_shops, balance)
        number_line += count_shops + TITLE_SIZE
        number_column = 0
        cur_day_title = QLabel("Итоговая статистика")
        cur_day_title.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        grid.addWidget(cur_day_title, number_line, number_column)
        number_column += TITLE_WIDTH
        (all_sold, all_deleted) = self.model.get_all_money()
        money_label = QLabel(
            "Продано на " + str(round(all_sold)) + "(руб.), списано на " + str(round(all_deleted)) + "(руб.)")
        grid.addWidget(money_label, number_line, number_column)
        number_line += LINE_SIZE
        table2 = QTableWidget(self)
        table2.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table2.setColumnCount(MAX_WIDTH - BALANCE_WIDTH)
        table2.setRowCount(count_products + TITLE_SIZE)
        create_itog_table(table2, names, all_sold_price, all_sold_count, all_deleted_price, all_deleted_count,
                          count_shops,
                          all_shop_requests, all_shop_given)

        grid.addWidget(table2, number_line, 0, count_shops, MAX_WIDTH - BALANCE_WIDTH)
        number_line += count_shops + TITLE_SIZE
        next_button = QPushButton("Следующий день")
        next_button.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        next_button.clicked.connect(self.next_day)
        next_button.setStyleSheet('background: green;')

        number_column = 0
        b_width = MAX_WIDTH // 3
        grid.addWidget(next_button, number_line, number_column, 1, b_width)
        number_column += b_width

        quick_end_button = QPushButton("До конца моделирования")
        quick_end_button.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        quick_end_button.clicked.connect(self.finish_modeling)
        quick_end_button.setStyleSheet('background: blue;')
        grid.addWidget(quick_end_button, number_line, number_column, 1, b_width)
        number_column += b_width

        finish_button = QPushButton("Завершить работу")
        finish_button.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        finish_button.clicked.connect(self.end_work)
        finish_button.setStyleSheet('background: red;')

        grid.addWidget(finish_button, number_line, number_column, 1, b_width)

        grid.setColumnMinimumWidth(1, 22)
        self.setLayout(grid)
        QApplication.desktop()
        self.setWindowTitle('Текущий день')
        self.resize(1200, 800)
        self.center()

    def end_work(self):
        self.close()

    def finish_modeling(self):
        number_rest_days = self.model.get_rest_count_days()
        for i in range(number_rest_days):
            self.model.next_day()
        end_win = EndWindow(self, self.model)
        self.close()
        end_win.show()
        return

    def next_day(self):
        if not self.model.is_end():
            next_day_model = self.model.next_day()
            day_win = DayWindow(self, next_day_model)
            self.close()
            day_win.show()
        else:
            end_win = EndWindow(self, self.model)
            self.close()
            end_win.show()
        return

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class BeginWindow(QWidget):
    def __init__(self, parent=None, first_flag=False):
        super().__init__(parent, Qt.Window)
        self.build(first_flag)

    def open_win(self):
        shops_count = int(self.shops.text())
        global MAX_WIDTH, SHOP_WIDTH, DELETED_WIDTH, SOLD_WIDTH, BALANCE_WIDTH, NAMES_WIDTH
        MAX_WIDTH = shops_count * 2 * SHOP_WIDTH + 2 * PRICE_WIDTH + 2 * SOLD_WIDTH + BALANCE_WIDTH + NAMES_WIDTH
        model = Model(int(self.products.text()), shops_count, int(self.days_count.text()), self.agiotage.value() / 100)
        day_win = DayWindow(self, model.next_day())
        self.close()
        day_win.show()

    def build(self, first_flag):
        products_title = QLabel("Количество продуктов(от 1 до 16)")
        self.products = QLineEdit()
        shops_title = QLabel("Количество магазинов")
        self.shops = QLineEdit()
        agiotage_title = QLabel("Степень ажиотажа")
        self.agiotage = QSlider(Qt.Horizontal, self)
        self.agiotage.setMinimum(0)
        self.agiotage.setMaximum(100)
        self.agiotage.setSingleStep(1)
        days_count_title = QLabel("Количество дней")
        self.days_count = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addWidget(products_title)
        hbox.addWidget(self.products)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(shops_title)
        hbox2.addWidget(self.shops)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(days_count_title)
        hbox3.addWidget(self.days_count)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(agiotage_title)
        hbox4.addWidget(self.agiotage)

        self.beginButton = QPushButton("Начать моделирование")
        self.beginButton.setFont(PyQt5.QtGui.QFont("Times", FONT_SIZE, PyQt5.QtGui.QFont.Bold))
        self.beginButton.clicked.connect(self.open_win)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.beginButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        self.setLayout(vbox)

        self.setGeometry(444, 300, 350, 300)
        self.center()
        self.setWindowTitle('Начало работы')
        if first_flag:
            self.show()

        return

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
