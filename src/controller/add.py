from psycopg2.extensions import connection
from PyQt5 import QtWidgets
from src.util.verify import UserInputError
from typing import Callable


class AddCompanyWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[int], None]):
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
            if len(comp_name) == 0:
                raise UserInputError("Please enter a company name.")
            if self.company_exist(comp_name):
                raise UserInputError("Company already exists.")
        except UserInputError as e:
            e.display_dialog()
            return

        comp_id = self.create_company(comp_name, comp_type)

        self.create_cb(comp_id)

    def company_exist(self, comp_name) -> bool:
        query = f"SELECT company_exists('{comp_name}');"

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def create_company(self, comp_name: str, comp_type: str) -> int:
        query = f"SELECT add_company('{comp_name}','{comp_type}');"

        self.cursor.execute(query)

        comp_id = int(self.cursor.fetchall()[0][0])
        self.cnx.commit()

        return comp_id

    def __del__(self):
        self.cursor.close()


class AddSiteWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[int], None], comp_id: int):
        super(AddSiteWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb
        self.comp_id = comp_id

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
        self.add_site_lay.addWidget(self.submit_bttn)

        self.setLayout(self.add_site_lay)

    def extract_input(self):
        state = self.state_led.text()
        street = self.street_led.text()
        addr_num = self.addr_num_led.text()
        zip_code = self.zip_led.text()

        return state, street, addr_num, zip_code

    def format_for_query(self, state, street, addr_num, zip_code):
        state = "'%s'" % state
        street = "NULL" if len(street) == 0 else "'%s'" % street
        addr_num = "NULL" if len(addr_num) == 0 else addr_num

        return state, street, addr_num, zip_code

    def submit_clicked(self):
        state, street, addr_num, zip_code = self.extract_input()

        try:
            if len(state) == 0:
                raise UserInputError("Please enter a state.")
            if len(zip_code) == 0:
                raise UserInputError("Please enter a zip code.")
            if self.site_exists(state, street, addr_num, zip_code):
                raise UserInputError("Site already exists.")
        except UserInputError as e:
            e.display_dialog()
            return

        site_id = self.create_site(state, street, addr_num, zip_code)

        self.create_cb(site_id)

    def site_exists(self, state, street, addr_num, zip_code):
        state, street, addr_num, zip_code = self.format_for_query(
            state, street, addr_num, zip_code)
        query = f"""SELECT site_exists({self.comp_id}, {state}, {
            street}, {addr_num}, {zip_code})"""

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def create_site(self, state: str, street: str, addr_num: int, zip_code: int):
        state, street, addr_num, zip_code = self.format_for_query(
            state, street, addr_num, zip_code)
        query = f"""SELECT add_site({self.comp_id}, {state}, {
            street}, {addr_num}, {zip_code})"""

        self.cursor.execute(query)

        print(query)
        site_id = int(self.cursor.fetchall()[0][0])
        self.cnx.commit()

        return site_id


class AddFoodWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[int], None], comp_id: int):
        super(AddFoodWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb
        self.comp_id = comp_id

        # State
        self.name_led = QtWidgets.QLineEdit()
        self.name_led.setPlaceholderText("Food")

        # Cuisine
        self.cuisines = ["American", "Italian",
                         "Mexican", "Ice Cream", "Other"]
        self.cuisines_gb = QtWidgets.QGroupBox()
        self.cuisines_lay = QtWidgets.QHBoxLayout()

        for cuisine in self.cuisines:
            cuisine_rb = QtWidgets.QRadioButton(cuisine)
            self.cuisines_lay.addWidget(cuisine_rb)
        self.cuisines_lay.itemAt(
            len(self.cuisines)-1).widget().setChecked(True)

        self.comp_type_gb.setLayout(self.cuisines_lay)

        # Submit button
        self.submit_bttn = QtWidgets.QPushButton("Submit")
        self.submit_bttn.clicked.connect(self.submit_clicked)

        # Main Layout
        self.add_food_lay = QtWidgets.QVBoxLayout()
        self.add_food_lay.addWidget(self.name_led)
        self.add_food_lay.addWidget(self.comp_type_gb)
        self.add_food_lay.addWidget(self.submit_bttn)

        self.setLayout(self.add_food_lay)

    def extract_input(self):
        food_name = self.name_led.text()
        cuisine = ""
        for rb_idx, rb_val in enumerate(self.cuisines):
            if self.cuisines_lay.itemAt(rb_idx).widget().isChecked():
                cuisine = rb_val
                break

        return food_name, cuisine

    def submit_clicked(self):
        food_name, cuisine = self.extract_input()

        try:
            if len(food_name) == 0:
                raise UserInputError("Please enter a food name.")
            if self.food_exists(food_name):
                raise UserInputError("Food item already exists.")
        except UserInputError as e:
            e.display_dialog()
            return

        food_id = self.create_food(food_name, cuisine)

        self.create_cb(food_id)

    def site_exists(self, food_name):
        query = f"SELECT food_exists({self.comp_id}, '{food_name}');"

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def create_site(self, food_name, cuisine):
        query = f"SELECT add_food({self.comp_id},'{food_name}', '{cuisine}');"

        self.cursor.execute(query)

        food_id = int(self.cursor.fetchall()[0][0])
        self.cnx.commit()

        return food_id

    def __del__(self):
        self.cursor.close()


class AddRatingWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[None], None], food_id: int, site_id: int, cust_id: int):
        super(AddSiteWidget, self).__init__()

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.create_cb = create_cb
        self.food_id = food_id
        self.site_id = site_id
        self.cust_id = cust_id

        # Price
        self.price_led = NumericLineEditWidget()
        self.price_led.setPlaceholderText("Price (Optional)")

        # Zip Code
        self.rating_led = NumericLineEditWidget()
        self.rating_led.setPlaceholderText("Rating 1-5")

        # Submit button
        self.submit_bttn = QtWidgets.QPushButton("Submit")
        self.submit_bttn.clicked.connect(self.submit_clicked)

        # Main Layout
        self.add_rating_lay = QtWidgets.QVBoxLayout()
        self.add_rating_lay.addWidget(self.price_led)
        self.add_rating_lay.addWidget(self.rating_led)
        self.add_rating_lay.addWidget(self.submit_bttn)

        self.setLayout(self.add_rating_lay)

    def extract_input(self):
        price = self.price_led.text()
        rating = self.rating_led.text()

        return price, rating

    def format_for_query(self, price, rating):
        price = "NULL" if len(price) == 0 else float(price)
        rating = int(rating)

        return price, rating

    def submit_clicked(self):
        price, rating = self.extract_input()

        try:
            if len(rating) == 0:
                raise UserInputError("Please enter a rating.")
            if self.rating_exists():
                raise UserInputError("Rating already exists.")
        except UserInputError as e:
            e.display_dialog()
            return

        self.create_rating(price, rating)

        self.create_cb()

    def rating_exists(self):
        query = f"""SELECT rating_exists({self.food_id}, {
            self.site_id}, {self.cust_id})"""

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def create_site(self, price, rating):
        price, rating = self.format_for_query(price, rating)
        query = f"""SELECT add_rating({self.food_id}, {self.site_id}, {
            self.cust_id}, {price}, {rating})"""

        self.cursor.execute(query)

        self.cursor.fetchall()[0][0]
        self.cnx.commit()


class NumericLineEditWidget(QtWidgets.QLineEdit):
    def __init__(self):
        super(NumericLineEditWidget, self).__init__()

        self.textEdited.connect(self.enforce_numeric)

    def enforce_numeric(self, text):
        numerical = "".join([ch for ch in text if ch in "0123456789."])
        self.setText(numerical)
