from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from psycopg2.extensions import connection
import os
from typing import List, Tuple

NUM_TOP_FOOD_ITEMS = 5
NUM_TOP_COMPANIES = 5


class DashboardWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection):
        super(DashboardWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/dashboard.ui')
        uic.loadUi(ui_filepath, self)

        self.cnx = cnx
        self.cursor = self.cnx.cursor()

        self.populate_table()

        # Utilities

        def add_cb(): return print("ADDING")
        def logout_cb(): return print("LOGGING OUT")

        self.utilLayout.addWidget(UtilityButton("Add", add_cb))
        self.utilLayout.addWidget(UtilityButton("Logout", logout_cb))

    def populate_table(self):
        # Request data from the table
        top_food_items_query = f"SELECT top_food_items({NUM_TOP_FOOD_ITEMS});"
        top_companies_query = f"SELECT top_companies({NUM_TOP_COMPANIES});"
        food_entries_query = f"SELECT food_entries();"

        self.cursor.execute(top_food_items_query)
        top_food_items = self.parse_table(self.cursor.fetchall())

        self.cursor.execute(top_companies_query)
        top_companies = self.parse_table(self.cursor.fetchall())

        self.cursor.execute(food_entries_query)
        food_entries = self.parse_table(self.cursor.fetchall())

        # Populate top food items
        for row in top_food_items:
            food_name, rating = row[0], round(float(row[1]), 1)
            self.topFoodItemsLayout.addWidget(
                TopFoodItem(food_name, rating))

        # Populate top companies
        for row in top_companies:
            comp_name, rating = row[0], round(float(row[1]), 1)
            self.topCompaniesLayout.addWidget(
                TopCompany(comp_name, rating))

        # Populate food entries
        self.foodEntriesTable.setRowCount(len(food_entries))
        for entry_idx, row in enumerate(food_entries):
            food_name, comp_name, num_ratings, avg_rating = row
            avg_rating = str(round(float(avg_rating), 1))
            self.foodEntriesTable.setItem(
                entry_idx, 0, QtWidgets.QTableWidgetItem(avg_rating))
            self.foodEntriesTable.setItem(
                entry_idx, 1, QtWidgets.QTableWidgetItem(num_ratings))
            self.foodEntriesTable.setItem(
                entry_idx, 2, QtWidgets.QTableWidgetItem(food_name))
            self.foodEntriesTable.setItem(
                entry_idx, 3, QtWidgets.QTableWidgetItem(comp_name))

    @ staticmethod
    def parse_table(table: List[Tuple[str]]) -> List[List[str]]:
        table = [[v.replace('"', '')
                  for v in row[0][1:-1].split(',')] for row in table]
        return table

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
