from PyQt5 import QtWidgets, uic
from typing import Callable
import os


class StartWindow(QtWidgets.QMainWindow):
    def __init__(self,
                 login_cb: Callable[[QtWidgets.QMainWindow], None],
                 register_cb: Callable[[QtWidgets.QMainWindow], None]):
        super(StartWindow, self).__init__()
        ui_filepath = os.path.join(os.path.dirname(__file__), '../ui/start.ui')
        uic.loadUi(ui_filepath, self)

        # Connect Signals to their corresponding slots.
        self.loginButton.clicked.connect(self.on_clicked_login)
        self.registerButton.clicked.connect(self.on_clicked_register)

        # Save callback functions from window manager
        self.login_cb = login_cb
        self.register_cb = register_cb

    def on_clicked_login(self):
        self.login_cb(self)

    def on_clicked_register(self):
        self.register_cb(self)
