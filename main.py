from PyQt5 import (QtWidgets, uic)
from src.database.connect import connect
from src.database.config import load_config
from psycopg2.extensions import connection
import sys

# Import windows
from src.controller.start import StartWindow
from src.controller.login import LoginWindow
from src.controller.register import RegisterWindow
from src.controller.dashboard import DashboardWindow


class WindowManager:
    def __init__(self, cnx: connection):
        self.cnx = cnx
        self.cursor = self.cnx.cursor()

        self.start_window = StartWindow(self.start_login, self.start_register)
        self.login_window = LoginWindow(self.cnx, self.start_dashboard)
        self.register_window = RegisterWindow(self.cnx, self.start_login)

    def start(self) -> None:
        self.start_window.show()

    def start_login(self, wfrom: QtWidgets.QMainWindow) -> None:
        wfrom.close()
        self.login_window.show()

    def start_register(self, wfrom: QtWidgets.QMainWindow) -> None:
        wfrom.close()
        self.register_window.show()

    def start_dashboard(self, wfrom: QtWidgets.QMainWindow, cust_id: int) -> None:
        wfrom.close()
        self.dashboard_window = DashboardWindow(
            self.cnx, cust_id, self.close_cb)
        self.dashboard_window.show()

    def close_cb(self):
        self.dashboard_window.close()

    def __del__(self):
        print("TERMINATED CONNECTION")
        self.cursor.close()
        self.cnx.close()


if __name__ == "__main__":
    config = load_config()
    conn = connect(config)
    app = QtWidgets.QApplication(sys.argv)
    win_man = WindowManager(conn)
    win_man.start()
    # dash = DashboardWindow(conn, 1)
    # dash.show()
    # rate = RatingWindow(conn)
    # rate.show()
    sys.exit(app.exec())
