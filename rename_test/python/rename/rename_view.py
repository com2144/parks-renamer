from PySide2.QtWidgets import *


class RenamePathView(QWidget):
    def __init__(self):
        super().__init__()
        self.line_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.path_layout = QHBoxLayout()
        self.main_layout = QGridLayout()


class RenameNewPathView(QWidget):
    def __init__(self):
        super().__init__()
        self.old_edit = QLineEdit()
        self.new_edit = QLineEdit()
        self.second_old_edit = QLineEdit()
        self.second_new_edit = QLineEdit()
        self.rename_button = QPushButton("Rename")
        self.plus_button = QPushButton("+")
        self.minus_button = QPushButton("-")
        self.second_minus_button = QPushButton("-")
        self.new_name_layout = QHBoxLayout()
        self.rename_button_layout = QHBoxLayout()
        self.second_rename_button_layout = QHBoxLayout()
        self.plus_button_layout = QHBoxLayout()
        self.minus_button_layout = QHBoxLayout()