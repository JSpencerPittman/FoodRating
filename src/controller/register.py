from PyQt5 import (QtWidgets, uic)
from src.util.verify import (UserInputError,
                             verify_first_name,
                             verify_middle_name,
                             verify_last_name,
                             verify_email,
                             verify_new_password,
                             verify_password_confirm)
from typing import Callable
from psycopg2.extensions import connection
import os


class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self, cnx: connection, login_cb: Callable[[QtWidgets.QMainWindow], None]) -> None:
        super(RegisterWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/register.ui')
        uic.loadUi(ui_filepath, self)

        # Save connection to the database
        self.cnx = cnx
        self.cursor = cnx.cursor()

        # Connect Signals to their corresponding slots.
        self.registerButton.clicked.connect(self.on_clicked_register)

        # Save callback functions from window manager
        self.login_cb = login_cb

    def extract_input(self):
        first_name = self.firstNameLineEdit.text().strip().lower()
        middle_name = self.middleNameLineEdit.text().strip().lower()
        last_name = self.lastNameLineEdit.text().strip().lower()
        email = self.emailLineEdit.text().strip().lower()
        password = self.passwordLineEdit.text().strip()
        password_confirm = self.passwordConfirmLineEdit.text().strip()

        return first_name, middle_name, last_name, email, password, password_confirm

    def on_clicked_register(self):
        first_name, middle_name, last_name, email, password, password_confirm = self.extract_input()

        # Verify user input
        try:
            verify_first_name(first_name)
            verify_middle_name(middle_name)
            verify_last_name(last_name)
            verify_email(email)
            verify_new_password(password)
            verify_password_confirm(password, password_confirm)
        except UserInputError as e:
            e.display_dialog()
            return

        # Ensure user doesn't already exist
        if self.user_exists(email):
            uie = UserInputError('User with this email already exists.')
            uie.display_dialog()
            return

        # Create new user
        self.create_user(email, password, first_name, middle_name, last_name)

        self.login_cb(self)

    def user_exists(self, email: str) -> bool:
        query = f"SELECT user_exists('{email}');"

        self.cursor.execute(query)

        return bool(self.cursor.fetchall()[0][0])

    def create_user(self, email: str, password: str, fname: str, mname: str, lname: str) -> None:
        query = f"SELECT add_user('{email}','{password}','{
            fname}','{mname}','{lname}');"

        self.cursor.execute(query)

        self.cursor.fetchall()
        self.cnx.commit()

    def __del__(self):
        self.cursor.close()
