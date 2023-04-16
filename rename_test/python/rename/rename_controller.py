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
        self.action_count = 0
        self.action_number = []

    def path_ui(self):
        self.rename_view.line_edit.setPlaceholderText("Enter a file path")
        self.rename_view.line_edit.textChanged.connect(self.on_text_changed(self.rename_model.path))

        self.rename_view.path_layout.addWidget(self.rename_view.line_edit)
        self.rename_view.path_layout.addWidget(self.rename_view.browse_button)

        self.rename_view.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.newname_view.use_button_layout.addWidget(self.newname_view.plus_button)
        self.newname_view.use_button_layout.addWidget(self.newname_view.minus_button)
        self.newname_view.use_button_layout.addWidget(self.newname_view.rename_button)

        self.newname_view.plus_button.clicked.connect(self.on_plus_button_clicked)
        self.newname_view.minus_button.clicked.connect(self.on_minus_button_clicked)

        self.newname_view.new_name_layout.addWidget(self.newname_view.old_edit)
        self.newname_view.new_name_layout.addWidget(self.newname_view.new_edit)
        self.newname_view.widget_hbox_layout.setLayout(self.newname_view.new_name_layout)
        self.newname_model.old_text_widget.append(self.newname_view.old_edit)
        self.newname_model.new_text_widget.append(self.newname_view.new_edit)
        self.newname_model.rename_hbox.append(self.newname_view.new_name_layout)
        self.newname_model.rename_hwidget.append(self.newname_view.widget_hbox_layout)

        self.newname_view.new_name_vbox_layout.addWidget(self.newname_view.widget_hbox_layout)
        self.newname_view.widget_vbox_layout.setLayout(self.newname_view.new_name_vbox_layout)

        self.newname_view.scroll_edit_layout.setWidgetResizable(True)
        self.newname_view.scroll_edit_layout.setWidget(self.newname_view.widget_vbox_layout)

        self.rename_view.main_layout.addLayout(self.rename_view.path_layout, 1, 2)
        self.rename_view.main_layout.addLayout(self.newname_view.use_button_layout, 2, 1)
        self.rename_view.main_layout.addWidget(self.newname_view.scroll_edit_layout, 2, 2)

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
        self.action_number.append('action')
        self.action_count = len(self.action_number)

        if self.action_count > 0:
            new_old_edit = QLineEdit()
            new_new_edit = QLineEdit()

            new_hbox_layout = QHBoxLayout()
            new_widget_hbox_layout = QWidget()

            self.newname_model.old_text_widget.append(new_old_edit)
            self.newname_model.new_text_widget.append(new_new_edit)
            self.newname_model.rename_hbox.append(new_hbox_layout)
            self.newname_model.rename_hwidget.append(new_widget_hbox_layout)

            for i in range(self.action_count):
                self.newname_view.second_old_edit = self.newname_model.old_text_widget[i + 1]
                self.newname_view.second_new_edit = self.newname_model.new_text_widget[i + 1]
                self.newname_model.rename_hbox[i + 1].addWidget(self.newname_view.second_old_edit)
                self.newname_model.rename_hbox[i + 1].addWidget(self.newname_view.second_new_edit)
                self.newname_model.rename_hwidget[i + 1].setLayout(self.newname_model.rename_hbox[i + 1])
                self.newname_view.new_name_vbox_layout.addWidget(self.newname_model.rename_hwidget[i + 1])
            self.newname_view.widget_vbox_layout.setLayout(self.newname_view.new_name_vbox_layout)
            self.newname_view.scroll_edit_layout.setWidget(self.newname_view.widget_vbox_layout)

    def on_minus_button_clicked(self):
        if self.action_count > 0:
            self.newname_model.old_text_widget[-1].setParent(None)
            self.newname_model.new_text_widget[-1].setParent(None)

            self.newname_model.rename_hbox[-1].removeWidget(self.newname_model.old_text_widget[-1])
            self.newname_model.rename_hbox[-1].removeWidget(self.newname_model.new_text_widget[-1])

            self.newname_model.old_text_widget.pop()
            self.newname_model.new_text_widget.pop()
            self.newname_model.rename_hbox.pop()
            self.newname_model.rename_hwidget.pop()

            self.action_number.pop()
            self.action_count = len(self.action_number)

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
        # 차례로 들어가도록 수정
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
