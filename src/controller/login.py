from PyQt5 import (QtWidgets, uic)
from src.util.verify import (UserInputError, verify_email, verify_password)
from psycopg2.extensions import connection
from typing import Callable
import os


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection, dashboard_cb: Callable[[QtWidgets.QMainWindow], None]) -> None:
        super(LoginWindow, self).__init__()
        ui_filepath = os.path.join(os.path.dirname(__file__), '../ui/login.ui')
        uic.loadUi(ui_filepath, self)

        # Connect Signals to their corresponding slots.
        self.loginButton.clicked.connect(self.on_clicked_login)

        # Save connection to the database
        self.cnx = cnx
        self.cursor = cnx.cursor()

        # Save callback functions from window manager
        self.dashboard_cb = dashboard_cb

    def extract_input(self):
        email = self.emailLineEdit.text().strip().lower()
        password = self.passwordLineEdit.text().strip().lower()

        return email, password

    def on_clicked_login(self):
        email, password = self.extract_input()

        try:
            verify_email(email)
            verify_password(password)
        except UserInputError as e:
            e.display_dialog()
            return

        if self.validate_credentials(email, password):
            self.dashboard_cb(self)
        else:
            err = UserInputError("invalid login.")
            err.display_dialog()
            return

    def validate_credentials(self, email: str, password: str) -> bool:
        query = f"SELECT valid_user('{email}', '{password}');"

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def __del__(self):
        self.cursor.close()
