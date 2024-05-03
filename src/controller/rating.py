from psycopg2.extensions import connection, cursor
from PyQt5 import QtWidgets, uic
from typing import List, Callable
from src.util.verify import UserInputError
from src.controller.add import AddCompanyWidget, AddSiteWidget
import os


class RatingWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection):
        super(RatingWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/rating.ui')
        uic.loadUi(ui_filepath, self)

        self.cnx = cnx
        self.cursor = self.cnx.cursor()

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

    # Company
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
        print(sites)
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
        pass

    def site_submitted(self, site_id: int):
        pass

    def site_created_cb(self, site_id: int):
        print(site_id)

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
