from PyQt5 import (QtWidgets, uic)
from src.util.verify import (UserInputError,
                             verify_first_name,
                             verify_middle_name,
                             verify_last_name,
                             verify_email,
                             verify_new_password,
                             verify_password_confirm)
import sys
import os


class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        ui_filepath = os.path.join(
            os.path.dirname(__file__), '../ui/register.ui')
        uic.loadUi(ui_filepath, self)

        # Connect Signals to their corresponding slots.
        self.registerButton.clicked.connect(self.on_clicked_register)

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
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())
