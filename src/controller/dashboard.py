from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from psycopg2.extensions import connection
import sys
import os


class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection):
        super(DashboardWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/dashboard.ui')
        uic.loadUi(ui_filepath, self)

        self.cnx = cnx
        self.cursor = self.cnx.cursor()

        # Top Food Items
        for x in range(5):
            self.topFoodItemsLayout.addWidget(
                TopFoodItem('5 Layer Burrito', 4.4))

        # Top Companies
        for x in range(10):
            self.topCompaniesLayout.addWidget(
                TopCompany('Taco Bell', 4.4))

        # Food Entries
        self.foodEntriesTable.setRowCount(10)
        for x in range(10):
            self.foodEntriesTable.setItem(
                x, 0, QtWidgets.QTableWidgetItem("4.4"))
            self.foodEntriesTable.setItem(
                x, 1, QtWidgets.QTableWidgetItem("146"))
            self.foodEntriesTable.setItem(
                x, 2, QtWidgets.QTableWidgetItem("Chalupa"))
            self.foodEntriesTable.setItem(
                x, 3, QtWidgets.QTableWidgetItem("Taco Bell"))

        # Utilities

        def add_cb(): return print("ADDING")
        def logout_cb(): return print("LOGGING OUT")

        self.utilLayout.addWidget(UtilityButton("Add", add_cb))
        self.utilLayout.addWidget(UtilityButton("Logout", logout_cb))

    def __del__(self):
        self.cursor.close()


class TopFoodItem(QtWidgets.QWidget):
    def __init__(self, food_name: str, rating: float):
        super(TopFoodItem, self).__init__()

        food_name_lbl = QtWidgets.QLabel(food_name)
        food_name_lbl.setFont(QFont("Times", 16))
        food_name_lbl.setWordWrap(True)
        food_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        rating_lbl = QtWidgets.QLabel(f"{round(rating, 2)} stars")
        rating_lbl.setFont(QFont("Times", 12))
        rating_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.addWidget(food_name_lbl)
        vlayout.addWidget(rating_lbl)

        self.setLayout(vlayout)
        self.setStyleSheet("background-color: red;")


class TopCompany(QtWidgets.QWidget):
    def __init__(self, comp_name: str, rating: float):
        super(TopCompany, self).__init__()

        rating_lbl = QtWidgets.QLabel(f"{round(rating, 2)} stars")
        rating_lbl.setFont(QFont("Times", 12))
        rating_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        comp_name_lbl = QtWidgets.QLabel(comp_name)
        comp_name_lbl.setFont(QFont("Times", 16))
        comp_name_lbl.setWordWrap(True)
        comp_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setSpacing(0)
        hlayout.addWidget(rating_lbl)
        hlayout.addWidget(comp_name_lbl)

        self.setLayout(hlayout)
        self.setStyleSheet("background-color: blue;")


class FoodEntry(object):
    def __init__(self, rating: float, num_ratings: int, name: str, company: str):
        self.rating = rating
        self.num_ratings = num_ratings
        self.name = name
        self.company = company


class UtilityButton(QtWidgets.QPushButton):
    def __init__(self, text, callback):
        super(UtilityButton, self).__init__()

        self.setText(text)
        self.clicked.connect(callback)


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = DashboardWindow()
#     window.show()
#     sys.exit(app.exec())
