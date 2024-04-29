from PyQt5 import QtWidgets, uic
import sys
import os


class StartWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()
        ui_filepath = os.path.join(os.path.dirname(__file__), '../ui/start.ui')
        uic.loadUi(ui_filepath, self)

        # Connect Signals to their corresponding slots.
        self.loginButton.clicked.connect(self.on_clicked_login)
        self.registerButton.clicked.connect(self.on_clicked_register)

    def on_clicked_login(self):
        pass

    def on_clicked_register(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
