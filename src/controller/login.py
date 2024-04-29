from PyQt5 import QtWidgets, uic
from src.util.verify import (UserInputError, verify_email)
import sys
import os


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        ui_filepath = os.path.join(os.path.dirname(__file__), '../ui/login.ui')
        uic.loadUi(ui_filepath, self)

        # Connect Signals to their corresponding slots.
        self.loginButton.clicked.connect(self.on_clicked_login)

    def extract_input(self):
        email = self.emailLineEdit.text().strip().lower()
        password = self.passwordLineEdit.text().strip().lower()

        return email, password

    def on_clicked_login(self):
        email, password = self.extract_input()

        try:
            verify_email(email)
            if not len(password):
                raise UserInputError('password not provided.')
        except UserInputError as e:
            print(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
