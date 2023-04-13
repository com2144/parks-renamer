from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QPushButton, QHBoxLayout
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
        self.newname_view.old_edit = QLineEdit()
        self.newname_view.new_edit = QLineEdit()
        re_name_button = QPushButton("Rename")

        self.newname_model.old_names.append(self.newname_view.old_edit)
        self.newname_model.new_names.append(self.newname_view.new_edit)
        self.newname_model.rename_button.append(re_name_button)

        row = len(self.newname_model.old_names)

        for i in reversed(range(self.newname_view.new_name_layout.count())):
            self.newname_view.new_name_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.newname_view.rename_button_layout.count())):
            self.newname_view.rename_button_layout.itemAt(i).widget().setParent(None)

        for i in range(row):
            old_edit = self.newname_model.old_names[i]
            new_edit = self.newname_model.new_names[i]
            re_name_button = self.newname_model.rename_button[-1]

            if self.rename_view.main_layout.indexOf(old_edit) != -1:
                self.rename_view.main_layout.removeWidget(old_edit)
                old_edit.setParent(None)
            if self.rename_view.main_layout.indexOf(new_edit) != -1:
                self.rename_view.main_layout.removeWidget(new_edit)
                new_edit.setParent(None)
            if self.rename_view.main_layout.indexOf(re_name_button) != -1:
                self.rename_view.main_layout.removeWidget(re_name_button)
                re_name_button.setParent(None)

            hbox = QHBoxLayout()
            hbox.addWidget(old_edit)
            hbox.addWidget(new_edit)

            self.rename_view.main_layout.addLayout(hbox, i + 3, 1)
            if row > 1:
                old_re_name_button = self.newname_model.rename_button[-2]
                if self.rename_view.main_layout.indexOf(old_re_name_button) != -1:
                    self.rename_view.main_layout.removeWidget(old_re_name_button)
                    old_re_name_button.setParent(None)
                    old_re_name_button.hide()

            self.rename_view.main_layout.addWidget(re_name_button, row + 3, 1)

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
        self.newname_view.old_name_edit.setText(file_name)
        # self.newname_model.set_new_name(file_name)


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
