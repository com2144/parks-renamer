from PySide2.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout


class RenameView(QLineEdit):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Enter a file path")
        self.text_edit.textChanged.connect(self.controller.on_text_changed)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.controller.on_browse_button_clicked)

        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.text_edit)
        self.path_layout.addWidget(self.browse_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.path_layout)


    def path_update(self):
        self.text_edit.setText(self.controller.get_text)

