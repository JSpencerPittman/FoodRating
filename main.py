from PyQt5 import (QtWidgets, uic)
from src.controller.dashboard import DashboardWindow
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
