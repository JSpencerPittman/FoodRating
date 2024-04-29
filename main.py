from PyQt5 import (QtWidgets, uic)
from src.controller.login import LoginWindow
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
