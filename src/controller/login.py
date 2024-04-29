from PyQt5 import QtWidgets, uic
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
        email = self.emailLineEdit.text()
        password = self.passwordLineEdit.text()

        return email, password

    def on_clicked_login(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
