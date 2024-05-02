from psycopg2.extensions import connection, cursor
from PyQt5 import QtWidgets, uic
from typing import List, Callable
from src.util.verify import UserInputError
from src.controller.add import AddCompanyWidget
import os


class RatingWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection):
        super(RatingWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/rating.ui')
        uic.loadUi(ui_filepath, self)

        self.cnx = cnx

        # Add Search Widget
        self.srch_comp = SearchWidget(
            ["Taco Bell", "KFC", "Mickeys", "Barbie", "Oppenheimer"], self.comp_doesnt_exist)

        # Add Company
        self.add_comp = AddCompanyWidget(self.cnx, self.comp_created_cb)
        self.add_comp.hide()

        # Main Layout for this widget
        self.main_layout = self.centralWidget.layout()
        self.main_layout.addWidget(self.srch_comp)
        self.main_layout.addWidget(self.add_comp)

    def comp_doesnt_exist(self):
        self.srch_comp.deleteLater()
        self.add_comp.show()

    def comp_created_cb(self, comp_name: str):
        print("CREATED ", comp_name)


class SearchWidget(QtWidgets.QWidget):
    def __init__(self, contents: List[str], not_here_cb: Callable[[None], None]):
        super(SearchWidget, self).__init__()

        self.contents = contents

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


# class AddCompanyWidget(QtWidgets.QWidget):
#     def __init__(self, cursor: cursor):
#         super(AddCompanyWidget, self).__init__()

#         # Company name
#         self.comp_name_led = QtWidgets.QLineEdit()
#         self.comp_name_led.setPlaceholderText("Company Name")

#         # Company Type
#         comp_types = ["American", "Italian", "Mexican", "Ice Cream", "Other"]
#         self.comp_type_lay = QtWidgets.QHBoxLayout()

#         for comp_type in comp_types:
#             comp_type_rb = QtWidgets.QRadioButton(comp_type)
#             self.comp_type_lay.addWidget(comp_type_rb)
#         self.comp_type_lay.itemAt(len(comp_types)-1).widget().setChecked(True)

#         # State
#         self.state_led = QtWidgets.QLineEdit()
#         self.state_led.setPlaceholderText("State")

#         # Street
#         self.street_led = QtWidgets.QLineEdit()
#         self.street_led.setPlaceholderText("Street (Optional)")

#         # Address number
#         self.addr_num_led = NumericLineEditWidget()
#         self.addr_num_led.setPlaceholderText("Address Number (Optional)")

#         # Zip code
#         self.zip_code_led = NumericLineEditWidget()
#         self.zip_code_led.setPlaceholderText("Zip Code")

#         # Submit button
#         self.submit_bttn = QtWidgets.QPushButton("Submit")

#         # Main Layout
#         self.add_site_lay = QtWidgets.QVBoxLayout()
#         self.add_site_lay.addWidget(self.comp_name_led)
#         self.add_site_lay.addLayout(self.comp_type_lay)
#         self.add_site_lay.addWidget(self.state_led)
#         self.add_site_lay.addWidget(self.street_led)
#         self.add_site_lay.addWidget(self.addr_num_led)
#         self.add_site_lay.addWidget(self.zip_code_led)
#         self.add_site_lay.addWidget(self.submit_bttn)

#         self.setLayout(self.add_site_lay)

#     def submit_clicked(self):
#         if self.comp_name_led.text() is None:
#             raise UserInputError("Please enter a company name")
#         if self.state_led.text() is None:
#             raise UserInputError("Please enter a state.")
#         if self.zip_code_led.text() is None:
#             raise UserInputError("Please enter a zip code.")

#     def does_company_exist(self, comp_name) -> bool:
#         pass


class NumericLineEditWidget(QtWidgets.QLineEdit):
    def __init__(self):
        super(NumericLineEditWidget, self).__init__()

        self.textEdited.connect(self.enforce_numeric)

    def enforce_numeric(self, text):
        numerical = "".join([ch for ch in text if ch in "0123456789."])
        self.setText(numerical)
