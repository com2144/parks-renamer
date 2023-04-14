from PySide2 import QtWidgets


class RenamePathView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.line_edit = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.path_layout = QtWidgets.QHBoxLayout()
        self.main_layout = QtWidgets.QGridLayout()


class RenameNewPathView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.old_edit = QtWidgets.QLineEdit()
        self.new_edit = QtWidgets.QLineEdit()
        self.second_old_edit = QtWidgets.QLineEdit()
        self.second_new_edit = QtWidgets.QLineEdit()
        self.rename_button = QtWidgets.QPushButton("Rename")
        self.plus_button = QtWidgets.QPushButton("Add Files")
        self.minus_button = QtWidgets.QPushButton("-")
        self.second_minus_button = QtWidgets.QPushButton("-")
        self.new_name_layout = QtWidgets.QHBoxLayout()
        self.rename_button_layout = QtWidgets.QHBoxLayout()
        self.second_rename_button_layout = QtWidgets.QHBoxLayout()
        self.plus_button_layout = QtWidgets.QHBoxLayout()