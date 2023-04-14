from PySide2.QtWidgets import *
from rename.rename_model import RenamePathModel
from rename.rename_view import RenamePathView
from rename.rename_model import RenameNewPathModel
from rename.rename_view import RenameNewPathView


class RenamePathController:
    def __init__(self):
        self.rename_model = RenamePathModel()
        self.rename_view = RenamePathView()
        self.newname_model = RenameNewPathModel()
        self.newname_view = RenameNewPathView()
        self.file_path = ''

    def path_ui(self):
        self.rename_view.line_edit.setPlaceholderText("Enter a file path")
        self.rename_view.line_edit.textChanged.connect(self.on_text_changed(self.rename_model.path))

        self.rename_view.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.newname_view.plus_button_layout.addWidget(self.newname_view.plus_button)
        self.newname_view.rename_button_layout.addWidget(self.newname_view.rename_button)

        self.rename_view.path_layout.addWidget(self.rename_view.line_edit)
        self.rename_view.path_layout.addWidget(self.rename_view.browse_button)

        self.newname_view.new_name_layout.addWidget(self.newname_view.old_edit)
        self.newname_view.new_name_layout.addWidget(self.newname_view.new_edit)
        self.newname_view.new_name_layout.addWidget(self.newname_view.minus_button)

        self.newname_view.plus_button.clicked.connect(self.on_plus_button_clicked)

        self.rename_view.main_layout.addLayout(self.rename_view.path_layout, 1, 1)
        self.rename_view.main_layout.addLayout(self.newname_view.plus_button_layout, 2, 1)
        self.rename_view.main_layout.addLayout(self.newname_view.new_name_layout, 3, 1)
        self.rename_view.main_layout.addLayout(self.newname_view.rename_button_layout, 4, 1)

        self.rename_view.setLayout(self.rename_view.main_layout)

    def on_text_changed(self, path):
        self.rename_model.set_path(path)

    def old_text_changed(self, name):
        self.newname_model.set_new_name(name)

    def on_browse_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_path, _ = QFileDialog.getOpenFileName(None, "Select file", "",
                                                        "All Files (*)",
                                                        options=options)
        if self.file_path:
            self.set_file_path(self.file_path)
            self.rename_model.set_path(self.file_path)

    def on_plus_button_clicked(self):
        self.newname_model.action_number.append('action')

        action_count = len(self.newname_model.action_number)

        if action_count > 0:
            self.newname_view.rename_button.setParent(None)
            self.newname_view.rename_button.hide()
            self.newname_view.rename_button_layout.setParent(None)
            self.newname_view.rename_button_layout.removeWidget(self.newname_view.rename_button)

        self.newname_view.second_old_edit = QLineEdit()
        self.newname_view.second_new_edit = QLineEdit()
        self.newname_view.second_minus_button = QPushButton('-')
        self.newname_view.second_name_layout = QHBoxLayout()
        self.newname_view.second_name_layout.addWidget(self.newname_view.second_old_edit)
        self.newname_view.second_name_layout.addWidget(self.newname_view.second_new_edit)
        self.newname_view.second_name_layout.addWidget(self.newname_view.second_minus_button)

        self.newname_view.rename_button = QPushButton("Rename")
        self.newname_view.rename_button_layout = QHBoxLayout()
        self.newname_view.rename_button_layout.addWidget(self.newname_view.rename_button)

        self.newname_model.old_text_widget.append(self.newname_view.second_old_edit)
        self.newname_model.new_text_widget.append(self.newname_view.second_new_edit)
        self.newname_model.minus_button.append(self.newname_view.second_minus_button)
        self.newname_model.rename_hbox.append(self.newname_view.second_name_layout)
        self.newname_model.rename_button.append(self.newname_view.rename_button)

        for i in range(action_count):
            self.newname_view.second_old_edit = self.newname_model.old_text_widget[i]
            self.newname_view.second_new_edit = self.newname_model.new_text_widget[i]
            self.newname_view.second_minus_button = self.newname_model.minus_button[i]
            self.newname_view.second_rename_button = self.newname_model.rename_button[-1]

            hbox = QHBoxLayout()
            hbox.addWidget(self.newname_view.second_old_edit)
            hbox.addWidget(self.newname_view.second_new_edit)
            hbox.addWidget(self.newname_view.second_minus_button)

            mhbox = QHBoxLayout()
            mhbox.addWidget(self.newname_view.second_rename_button)

            self.rename_view.main_layout.addLayout(hbox, i+4, 1)
            self.rename_view.main_layout.addLayout(mhbox, i+5, 1)

    def set_file_path(self, file_path):
        front_split_path = file_path.split('/')[:-1]
        file_name = file_path.split('/')[-1]
        namelist = file_name.split('.')
        file_ext = namelist[-1]
        file_ext = ''.join(file_ext)
        del namelist[-1]
        file_name = ''.join(namelist)
        front_merge_path = '/'.join(front_split_path)
        self.rename_view.line_edit.setText(front_merge_path)
        self.rename_model.set_path(front_merge_path)
        self.newname_view.old_edit.setText(file_name)
        self.newname_model.set_new_name(file_name)


def main():
    app = QApplication()
    window = QMainWindow()
    controller = RenamePathController()
    window.setCentralWidget(controller.path_ui())
    controller.rename_view.setWindowTitle("Renamer")
    controller.rename_view.show()
    app.exec_()


if __name__ == '__main__':
    main()
