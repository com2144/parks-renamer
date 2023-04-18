import sys
import os
from PySide2.QtWidgets import *

class CustomFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Directory and View Files")
        self.directory_path = None

        self.file_dialog = QFileDialog(self, "Select Directory")
        self.file_dialog.setOption(QFileDialog.ShowDirsOnly)
        self.file_dialog.setFileMode(QFileDialog.Directory)
        self.file_dialog.setAcceptMode(QFileDialog.AcceptOpen)

        # QDialogButtonBox를 찾아 Choose 버튼에 연결된 기본 슬롯을 무시합니다.
        button_box = self.file_dialog.findChild(QDialogButtonBox)
        button_box.accepted.disconnect()
        button_box.accepted.connect(self.open_file_list_dialog)

    def open_file_list_dialog(self):
        self.directory_path = self.file_dialog.selectedFiles()[0]
        if os.path.isdir(self.directory_path):
            list_dialog = QDialog(self)
            list_dialog.setWindowTitle("Files in selected directory")

            label = QLabel("Files in selected directory:")
            list_widget = QListWidget()
            list_widget.setSelectionMode(QAbstractItemView.NoSelection)
            files = os.listdir(self.directory_path)
            for file in files:
                if os.path.isfile(os.path.join(self.directory_path, file)):
                    list_widget.addItem(file)

            close_button = QPushButton("Close")
            close_button.clicked.connect(list_dialog.accept)

            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(list_widget)
            layout.addWidget(close_button)
            list_dialog.setLayout(layout)

            list_dialog.exec_()
            self.accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.directory_path = ''
        self.directory_label = QLabel("Selected Directory: None")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.on_browse_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.directory_label)
        layout.addWidget(self.browse_button)
        self.setLayout(layout)

    def on_browse_button_clicked(self):
        custom_dialog = CustomFileDialog()
        result = custom_dialog.exec_()
        if result == QDialog.Accepted:
            self.directory_path = custom_dialog.directory_path
            self.directory_label.setText(f"Selected Directory: {self.directory_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
