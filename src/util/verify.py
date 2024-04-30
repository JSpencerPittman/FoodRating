from PyQt5 import QtWidgets


class UserInputError(Exception):
    def __init__(self, message):
        super(UserInputError, self).__init__(message)
        self.message = message

    def display_dialog(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Invalid Input")
        dlg.setText(str(self.message))
        dlg_btn = dlg.exec()

        if dlg_btn == QtWidgets.QMessageBox.Ok:
            return


def verify_email(email: str) -> None:
    if not len(email):
        raise UserInputError("no email provided.")

    try:
        at_idx = email.index('@')
        dot_idx = email.index('.')

        if at_idx == 0 or dot_idx < at_idx or (dot_idx - at_idx) == 1 or dot_idx == len(email)-1:
            raise ValueError('')

    except ValueError:
        raise UserInputError('invalid email provided.')


def verify_first_name(firstname: str) -> None:
    if not len(firstname):
        raise UserInputError("no first name provided.")
    if not firstname.isalpha():
        raise UserInputError(
            'first name must only contain alphabetical characters.')


def verify_middle_name(middlename: str) -> None:
    if not middlename.isalpha():
        raise UserInputError(
            'middle name must only contain alphabetical characters.')


def verify_last_name(lastname: str) -> None:
    if not len(lastname):
        raise UserInputError("no last name provided.")
    if not lastname.isalpha():
        raise UserInputError(
            'last name must only contain alphabetical characters.')


def verify_password(password: str) -> None:
    if not len(password):
        raise UserInputError("no password provided.")


def verify_new_password(password: str) -> None:
    if not len(password):
        raise UserInputError("no password provided.")

    if len(password) < 4:
        raise UserInputError('password must be at least 4 characters long.')
    if sum([char.isspace() for char in password]):
        raise UserInputError('password can\'t contain whitespace.')


def verify_password_confirm(password: str, confirm: str):
    if password != confirm:
        raise UserInputError('password confirmation is not the same.')
