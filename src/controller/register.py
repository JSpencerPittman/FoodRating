from PyQt5 import QtWidgets, uic
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
        first_name = self.firstNameLineEdit.text()
        middle_name = self.middleNameLineEdit.text()
        last_name = self.lastNameLineEdit.text()
        email = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()
        password_confirm = self.passwordConfirmLineEdit.text()

        return first_name, middle_name, last_name, email, password, password_confirm

    def on_clicked_register(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())
