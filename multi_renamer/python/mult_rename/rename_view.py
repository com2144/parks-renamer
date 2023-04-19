from PySide2.QtWidgets import *
import os


# class RenamePathView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.line_edit = QLineEdit()
#         self.browse_button = QPushButton("Browse")
#         self.path_layout = QHBoxLayout()
#         self.main_layout = QGridLayout()

class RenamePathView(QWidget):
    def __init__(self):
        super().__init__()
        self.line_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.path_layout = QHBoxLayout()
        self.main_layout = QGridLayout()


class FileListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Files in Directory")
        self.list_widget = QListWidget(self)
        self.dialog_layout = QVBoxLayout()
        self.dialog_layout.addWidget(self.list_widget)
        self.setLayout(self.dialog_layout)
        self.setModal(False)

    def set_files(self, file_list):
        for file in file_list:
            file_name, file_ext = os.path.splitext(file)
            if not file_ext == '':
                self.list_widget.addItem(file_name)


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
        self.rename_button = QPushButton("Rename")
        self.plus_button = QPushButton("+")
        self.minus_button = QPushButton("-")
        self.use_button_layout = QVBoxLayout()
