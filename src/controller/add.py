from psycopg2.extensions import connection
from PyQt5 import QtWidgets
from src.util.verify import UserInputError
from typing import Callable


class AddCompanyWidget(QtWidgets.QWidget):
    def __init__(self, cnx: connection, create_cb: Callable[[str], None]):
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
        self.add_site_lay = QtWidgets.QVBoxLayout()
        self.add_site_lay.addWidget(self.comp_name_led)
        self.add_site_lay.addWidget(self.comp_type_gb)
        self.add_site_lay.addWidget(self.submit_bttn)

        self.setLayout(self.add_site_lay)

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


# class AddSiteWidget(QtWidgets.QWidget):
#     def __init__(self, cursor: cursor):
#         super(AddCompanyWidget, self).__init__()
