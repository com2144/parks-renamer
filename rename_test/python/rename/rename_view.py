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
        self.new_name_layout = QHBoxLayout()
        self.widget_hbox_layout = QWidget()
        self.new_name_vbox_layout = QVBoxLayout()
        self.widget_vbox_layout = QWidget()
        self.scroll_edit_layout = QScrollArea()
        self.second_old_edit = QLineEdit()
        self.second_new_edit = QLineEdit()
        self.second_new_name_hbox_layout = QHBoxLayout()
        self.second_widget_hbox_layout = QWidget()
        self.second_new_name_vbox_layout = QVBoxLayout()
        self.second_widget_vbox_layout = QWidget()
        self.rename_button = QPushButton("Rename")
        self.plus_button = QPushButton("+")
        self.minus_button = QPushButton("-")
        self.use_button_layout = QVBoxLayout()
