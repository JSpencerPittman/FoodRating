from psycopg2.extensions import connection, cursor
from PyQt5 import QtWidgets, uic
from typing import List, Callable
from src.util.verify import UserInputError
from src.controller.add import AddCompanyWidget, AddSiteWidget, AddFoodWidget, AddRatingWidget
import os


class RatingWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection, cust_id, return_cb):
        super(RatingWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/rating.ui')
        uic.loadUi(ui_filepath, self)

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.cust_id = cust_id
        self.return_cb = return_cb

        # Company Search Widget
        self.cursor.execute("SELECT company_id, comp_name FROM company;")
        companies = self.cursor.fetchall()
        comp_ids = [row[0] for row in companies]
        comp_names = [row[1] for row in companies]
        self.srch_comp = SearchWidget(
            comp_ids, comp_names, self.comp_doesnt_exist, self.comp_submitted)

        # Main Layout for this widget
        self.main_layout = self.centralWidget.layout()
        self.main_layout.addWidget(self.srch_comp)

        # Save data
        self.comp_id = None

    def comp_doesnt_exist(self):
        self.srch_comp.deleteLater()

        # Add Company Widget
        self.add_comp = AddCompanyWidget(self.cnx, self.comp_created_cb)
        self.main_layout.addWidget(self.add_comp)

    def comp_submitted(self, comp_id: int):
        self.comp_id = comp_id

        self.srch_comp.deleteLater()

        self.cursor.execute(f"SELECT * FROM site WHERE company_id={comp_id}")
        sites = self.cursor.fetchall()

        site_ids = [row[0] for row in sites]
        locations = []
        for row in sites:
            locations.append(f"{row[2]}, {row[3]} {row[4]} {row[5]}")

        self.srch_sites = SearchWidget(
            site_ids, locations, self.site_doesnt_exist, self.site_submitted)
        self.main_layout.addWidget(self.srch_sites)

    def comp_created_cb(self, comp_id: int):
        self.comp_id = comp_id

        self.add_comp.deleteLater()

        # Add Site Widget
        self.add_site = AddSiteWidget(
            self.cnx, self.site_created_cb, self.comp_id)
        self.main_layout.addWidget(self.add_site)

    def site_doesnt_exist(self):
        self.srch_sites.deleteLater()

        # Add Company Widget
        self.add_site = AddSiteWidget(
            self.cnx, self.site_created_cb, self.comp_id)
        self.main_layout.addWidget(self.add_site)

    def site_submitted(self, site_id: int):
        self.site_id = site_id

        self.srch_sites.deleteLater()

        self.cursor.execute(
            f"SELECT * FROM food WHERE company_id={self.comp_id}")
        foods = self.cursor.fetchall()

        food_ids = [row[0] for row in foods]
        food_names = []
        for row in foods:
            food_names.append(
                f"{row[2]}{f', {row[3]}' if row[3] != "NULL" else ''}")

        self.srch_foods = SearchWidget(
            food_ids, food_names, self.food_doesnt_exist, self.food_submitted)
        self.main_layout.addWidget(self.srch_foods)

    def site_created_cb(self, site_id: int):
        self.site_id = site_id

        self.add_site.deleteLater()

        # Add Food Widget
        self.add_food = AddFoodWidget(
            self.cnx, self.food_created_cb, self.comp_id)
        self.main_layout.addWidget(self.add_food)

    def food_doesnt_exist(self):
        self.srch_foods.deleteLater()

        # Add Rating Widget
        self.add_food = AddFoodWidget(
            self.cnx, self.food_created_cb, self.comp_id)
        self.main_layout.addWidget(self.add_food)

    def food_submitted(self, food_id: int):
        self.food_id = food_id

        self.srch_foods.deleteLater()

        if self.rating_exists():
            uie = UserInputError("You have already rated this food item.")
            uie.display_dialog()
            self.return_cb()
        else:
            self.add_rating = AddRatingWidget(
                self.cnx, self.rating_created_cb, self.food_id, self.site_id, self.cust_id)
            self.main_layout.addWidget(self.add_rating)

    def food_created_cb(self, food_id: int):
        self.food_id = food_id

        self.add_food.deleteLater()

        self.add_rating = AddRatingWidget(
            self.cnx, self.rating_created_cb, self.food_id, self.site_id, self.cust_id)
        self.main_layout.addWidget(self.add_rating)

    def rating_created_cb(self):
        self.return_cb()

    def rating_exists(self):
        query = f"""SELECT rating_exists({self.food_id}, {
            self.site_id}, {self.cust_id})"""

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def __del__(self):
        self.cursor.close()

    def __del__(self):
        self.cursor.close()


class SearchWidget(QtWidgets.QWidget):
    def __init__(self, ids: List[int], contents: List[str], not_here_cb: Callable[[int], None], submit_cb: Callable[[str], None]):
        super(SearchWidget, self).__init__()

        self.ids = ids
        self.contents = contents
        self.submit_cb = submit_cb

        # Searching line edit
        self.search_led = QtWidgets.QLineEdit()
        self.search_led.textChanged.connect(self.search_list)

        # Search options
        self.search_lst = QtWidgets.QListWidget()
        self.search_lst.addItems(contents)
        self.search_lst.itemClicked.connect(self.select_item)

        # Missing entry button
        self.missing_bttn = QtWidgets.QPushButton("Not here?")
        self.missing_bttn.clicked.connect(not_here_cb)

        # Submit button
        self.submit_bttn = QtWidgets.QPushButton("Select")
        self.submit_bttn.clicked.connect(self.submit_clicked)

        # Layout
        self.search_lay = QtWidgets.QVBoxLayout()
        self.search_lay.addWidget(self.search_led)
        self.search_lay.addWidget(self.search_lst)
        self.search_lay.addWidget(self.missing_bttn)
        self.search_lay.addWidget(self.submit_bttn)

        # Connect to this widget
        self.setLayout(self.search_lay)

    def search_list(self, search_text):
        search_text = search_text.lower().strip()

        matches = [item for item in self.contents if search_text in item.lower()]

        self.search_lst.clear()
        self.search_lst.addItems(matches)

    def select_item(self, item):
        self.search_led.setText(item.text())

    def submit_clicked(self):
        try:
            if self.search_lst.count() == 0:
                raise UserInputError("Entry doesn't exist.")
            elif self.search_lst.count() > 1:
                raise UserInputError("Please select only one entry.")
        except UserInputError as e:
            e.display_dialog()
            return

        search_id = self.ids[self.contents.index(self.search_led.text())]
        self.submit_cb(search_id)
