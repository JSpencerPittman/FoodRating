from psycopg2.extensions import connection
from PyQt5 import QtWidgets
from src.util.verify import UserInputError
from typing import Callable


class AddCompanyWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[None], None]):
        super(AddCompanyWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb

        # Company name
        self.comp_name_led = QtWidgets.QLineEdit()
        self.comp_name_led.setPlaceholderText("Company Name")

        # Company Type
        self.comp_types = ["Restaurant", "Fast Food", "Other"]
        self.comp_type_gb = QtWidgets.QGroupBox()
        self.comp_type_lay = QtWidgets.QHBoxLayout()

        for comp_type in self.comp_types:
            comp_type_rb = QtWidgets.QRadioButton(comp_type)
            self.comp_type_lay.addWidget(comp_type_rb)
        self.comp_type_lay.itemAt(
            len(self.comp_types)-1).widget().setChecked(True)

        self.comp_type_gb.setLayout(self.comp_type_lay)
        self.comp_type_gb.setChecked(True)

        # Submit button
        self.submit_bttn = QtWidgets.QPushButton("Submit")
        self.submit_bttn.clicked.connect(self.submit_clicked)

        # Main Layout
        self.add_comp_lay = QtWidgets.QVBoxLayout()
        self.add_comp_lay.addWidget(self.comp_name_led)
        self.add_comp_lay.addWidget(self.comp_type_gb)
        self.add_comp_lay.addWidget(self.submit_bttn)

        self.setLayout(self.add_comp_lay)

    def extract_input(self):
        comp_name = self.comp_name_led.text()
        comp_type = ""
        for rb_idx, rb_val in enumerate(self.comp_types):
            if self.comp_type_lay.itemAt(rb_idx).widget().isChecked():
                comp_type = rb_val
                break

        return comp_name, comp_type

    def submit_clicked(self):
        comp_name, comp_type = self.extract_input()

        try:
            if comp_name is None:
                raise UserInputError("Please enter a company name.")
            if self.company_exist(comp_name):
                raise UserInputError("Company already exists.")
        except UserInputError as e:
            e.display_dialog()
            return

        self.create_company(comp_name, comp_type)

        self.create_cb(comp_name)

    def company_exist(self, comp_name) -> bool:
        query = f"SELECT company_exists('{comp_name}');"

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def create_company(self, comp_name: str, comp_type: str):
        query = f"SELECT add_company('{comp_name}','{comp_type}');"

        self.cursor.execute(query)

        self.cursor.fetchall()
        self.cnx.commit()

    def __del__(self):
        self.cursor.close()


class AddSiteWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[None], None]):
        super(AddCompanyWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb

        # State
        self.state_led = QtWidgets.QLineEdit()
        self.state_led.setPlaceholderText("State")

        # Street
        self.street_led = QtWidgets.QLineEdit()
        self.street_led.setPlaceholderText("Street (Optional)")

        # Address Number
        self.addr_num_led = NumericLineEditWidget()
        self.addr_num_led.setPlaceholderText("Address Number (Optional)")

        # Zip Code
        self.zip_led = NumericLineEditWidget()
        self.zip_led.setPlaceholderText("Zip Code")

        # Submit button
        self.submit_bttn = QtWidgets.QPushButton("Submit")
        self.submit_bttn.clicked.connect(self.submit_clicked)

        # Main Layout
        self.add_site_lay = QtWidgets.QVBoxLayout()
        self.add_site_lay.addWidget(self.state_led)
        self.add_site_lay.addWidget(self.street_led)
        self.add_site_lay.addWidget(self.addr_num_led)
        self.add_site_lay.addWidget(self.zip_led)

        self.setLayout(self.add_site_lay)

    def extract_input(self):
        state = self.state_led
        street = self.street_led
        addr_num = self.addr_num_led
        zip_code = self.zip_led

        return state, street, addr_num, zip_code

    def submit_clicked(self):
        state, street, addr_num, zip_code = self.extract_input()

        try:
            if state is None:
                raise UserInputError("Please enter a state.")
            if zip_code is None:
                raise UserInputError("Please enter a zip code.")
            if self.site_exists(state, street, addr_num, zip_code):
                raise UserInputError("Site already exists.")
        except UserInputError as e:
            e.display_dialog()
            return

        self.create_site(state, street, addr_num, zip_code)

        self.create_cb()

    def site_exists(self):
        pass


class AddFoodWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[None], None]):
        super(AddFoodWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb

    def extract_input(self):
        pass

    def submit_clicked(self):
        pass

    def rating_exists(self):
        pass


class AddRatingWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[None], None]):
        super(AddRatingWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb

        # Price
        self.price_led = NumericLineEditWidget()
        self.price_led.setPlaceholderText("Price (Optional)")

        # Rating
        self.rating_led = NumericLineEditWidget()
        self.rating_led.setPlaceholderText("Rating")

        # Main Layout
        self.add_rating_lay = QtWidgets.QVBoxLayout()
        self.add_rating_lay.addWidget(self.price_led)
        self.add_rating_lay.addWidget(self.rating_led)

        self.setLayout(self.add_rating_lay)

    def extract_input(self):
        price = self.price_led.text()
        rating = self.rating_led.text()

        return price, rating

    def submit_clicked(self):
        price, rating = self.extract_input()

        try:
            if rating is None:
                raise UserInputError("Please enter a rating.")
        except UserInputError as e:
            e.display_dialog()
            return

        self.create_cb()


class NumericLineEditWidget(QtWidgets.QLineEdit):
    def __init__(self):
        super(NumericLineEditWidget, self).__init__()

        self.textEdited.connect(self.enforce_numeric)

    def enforce_numeric(self, text):
        numerical = "".join([ch for ch in text if ch in "0123456789."])
        self.setText(numerical)
