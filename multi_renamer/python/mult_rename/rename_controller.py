from PySide2.QtWidgets import *
from mult_rename.rename_model import RenamePathModel
from mult_rename.rename_view import RenamePathView
from mult_rename.rename_model import RenameNewPathModel
from mult_rename.rename_view import RenameNewPathView
from mult_rename.rename_view import FileListDialog
from mult_rename.rename_view import BrowseDialog
import os


class RenamePathController:
    def __init__(self):
        self.rename_model = RenamePathModel()
        self.rename_view = RenamePathView()
        self.newname_model = RenameNewPathModel()
        self.newname_view = RenameNewPathView()

        self.dir_path = self.rename_model.path
        self.action_count = 0
        self.browse_count = False

        self.file_list_dialog = None

        self.deleted_old_text_widget = []
        self.deleted_new_text_widget = []
        self.deleted_rename_hbox = []
        self.deleted_rename_hwidget = []

        self.file_count = 0

        self.path_ui()

    def path_ui(self):
        self.rename_view.line_edit.setPlaceholderText("Enter a file path")

        self.rename_view.path_layout.addWidget(self.rename_view.line_edit)
        self.rename_view.path_layout.addWidget(self.rename_view.browse_button)

        self.rename_view.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.newname_view.use_button_layout.addWidget(self.newname_view.plus_button)
        self.newname_view.use_button_layout.addWidget(self.newname_view.minus_button)
        self.newname_view.use_button_layout.addWidget(self.newname_view.rename_button)

        self.newname_view.plus_button.clicked.connect(self.on_plus_button_clicked)
        self.newname_view.minus_button.clicked.connect(self.on_minus_button_clicked)
        self.newname_view.rename_button.clicked.connect(self.on_rename_button_clicked)

        self.newname_view.new_name_layout.addWidget(self.newname_view.old_edit)
        self.newname_view.new_name_layout.addWidget(self.newname_view.new_edit)
        self.newname_view.widget_hbox_layout.setLayout(self.newname_view.new_name_layout)
        self.newname_model.old_text_widget.append(self.newname_view.old_edit)
        self.newname_model.new_text_widget.append(self.newname_view.new_edit)
        self.newname_model.rename_hbox.append(self.newname_view.new_name_layout)
        self.newname_model.rename_hwidget.append(self.newname_view.widget_hbox_layout)

        self.newname_view.new_name_vbox_layout.setSpacing(0)
        self.newname_view.new_name_vbox_layout.addWidget(self.newname_view.widget_hbox_layout)
        self.newname_view.widget_vbox_layout.setLayout(self.newname_view.new_name_vbox_layout)

        self.newname_view.scroll_edit_layout.setWidgetResizable(True)
        self.newname_view.scroll_edit_layout.setWidget(self.newname_view.widget_vbox_layout)

        self.rename_view.main_layout.addLayout(self.rename_view.path_layout, 1, 2)
        self.rename_view.main_layout.addLayout(self.newname_view.use_button_layout, 2, 1)
        self.rename_view.main_layout.addWidget(self.newname_view.scroll_edit_layout, 2, 2)

        self.rename_view.setLayout(self.rename_view.main_layout)

    def on_browse_button_clicked(self):
        self.browse_count = True
        self.newname_model.old_full_path.clear()

        if self.file_list_dialog is not None:
            self.file_list_dialog.close()

        browse_option = BrowseDialog()
        self.dir_path = browse_option.option

        if self.dir_path == '':
            self.show_warning('Choose the directory')
            self.window_all_clear()
            return

        if not self.check_files_exist(self.dir_path):
            self.show_warning("The selected directory contains no files.")
            browse_option.close()
        else:
            self.set_file_path(self.dir_path)
            self.rename_view.line_edit.setText(self.dir_path)
            self.show_files_in_directory(self.dir_path)

    def show_files_in_directory(self, directory):
        file_list = os.listdir(directory)

        self.file_list_dialog = FileListDialog(self.rename_view)
        self.file_list_dialog.set_files(file_list)

        self.file_list_dialog.show()
        self.file_list_dialog.finished.connect(self.on_file_list_dialog_finished)

    def on_file_list_dialog_finished(self):
        self.file_list_dialog = None

    @staticmethod
    def check_files_exist(dir_path):
        if os.path.exists(dir_path):
            for entry in os.listdir(dir_path):
                confine_path = dir_path + '/' + entry
                _, file_ext = os.path.splitext(confine_path)
                if file_ext != '':
                    return True
            return False

    def set_file_path(self, path):
        if os.path.isdir(path):
            file_list = os.listdir(path)
        else:
            dir_path = os.path.dirname(path)
            file_list = os.listdir(dir_path)

        for index, file_name in enumerate(file_list):
            full_path = path + '/' + file_name
            if os.path.exists(full_path):
                self.newname_model.old_full_path.append(full_path)

    def on_plus_button_clicked(self):
        self.action_count += 1

        if self.action_count > 0 and self.deleted_old_text_widget and self.deleted_new_text_widget and self.deleted_rename_hbox and self.deleted_rename_hwidget:
            for i in range(self.action_count + 1):
                self.newname_model.old_text_widget.append(self.deleted_old_text_widget[i])
                self.newname_model.new_text_widget.append(self.deleted_new_text_widget[i])
                self.newname_model.rename_hbox.append(self.deleted_rename_hbox[i])
                self.newname_model.rename_hwidget.append(self.deleted_rename_hwidget[i])
        elif self.action_count > 0:
            new_old_edit = QLineEdit()
            new_new_edit = QLineEdit()
            new_hbox_layout = QHBoxLayout()
            new_widget_hbox_layout = QWidget()

            self.newname_model.old_text_widget.append(new_old_edit)
            self.newname_model.new_text_widget.append(new_new_edit)
            self.newname_model.rename_hbox.append(new_hbox_layout)
            self.newname_model.rename_hwidget.append(new_widget_hbox_layout)

        self.deleted_old_text_widget.clear()
        self.deleted_new_text_widget.clear()
        self.deleted_rename_hbox.clear()
        self.deleted_rename_hwidget.clear()

        for i in range(self.action_count):
            self.newname_model.rename_hbox[i + 1].addWidget(self.newname_model.old_text_widget[i + 1])
            self.newname_model.rename_hbox[i + 1].addWidget(self.newname_model.new_text_widget[i + 1])
            self.newname_model.rename_hwidget[i + 1].setLayout(self.newname_model.rename_hbox[i + 1])
            self.newname_view.new_name_vbox_layout.addWidget(self.newname_model.rename_hwidget[i + 1])
        self.newname_view.new_name_vbox_layout.setSpacing(0)
        self.newname_view.widget_vbox_layout.setLayout(self.newname_view.new_name_vbox_layout)
        self.newname_view.scroll_edit_layout.setWidgetResizable(True)
        self.newname_view.scroll_edit_layout.setWidget(self.newname_view.widget_vbox_layout)

    def on_minus_button_clicked(self):
        if self.action_count > 0:
            if self.newname_model.old_text_widget[-1].text():
                self.newname_model.old_text_widget[-1].clear()
                self.newname_model.new_text_widget[-1].clear()

            self.newname_model.old_text_widget[-1].setParent(None)
            self.newname_model.new_text_widget[-1].setParent(None)

            self.newname_model.rename_hbox[-1].removeWidget(self.newname_model.old_text_widget[-1])
            self.newname_model.rename_hbox[-1].removeWidget(self.newname_model.new_text_widget[-1])
            self.newname_view.new_name_vbox_layout.takeAt(self.newname_view.new_name_vbox_layout.count() - 1)

            self.newname_model.old_text_widget.pop()
            self.newname_model.new_text_widget.pop()
            self.newname_model.rename_hbox.pop()
            self.newname_model.rename_hwidget.pop()

            self.action_count -= 1

    def on_rename_button_clicked(self):
        for old_text in self.newname_model.old_text_widget:
            self.newname_model.old_file_user_name.append(old_text.text())
        for new_text in self.newname_model.new_text_widget:
            self.newname_model.new_file_user_name.append(new_text.text())

        if self.browse_count:
            for i in range(self.action_count+1):
                if self.newname_model.old_file_user_name[i] != '' and self.newname_model.new_file_user_name[i] != '' and len(self.newname_model.old_full_path) != len(self.newname_model.new_full_path):
                    for full_path in self.newname_model.old_full_path:
                        if any(user_file_name in full_path for user_file_name in self.newname_model.old_file_user_name[i]):
                            origin_file_name = os.path.basename(full_path)
                            without_origin_file_ext, origin_file_ext = os.path.splitext(origin_file_name)
                            new_file_name = without_origin_file_ext.replace(self.newname_model.old_file_user_name[i], self.newname_model.new_file_user_name[i])
                            new_full_path = '/'.join(full_path.split("/")[:-1]) + '/' + new_file_name + origin_file_ext
                            self.newname_model.new_full_path.append(new_full_path)
                            os.rename(full_path, new_full_path)
                        else:
                            self.show_warning('File name does not exist.')
                            self.window_all_clear()
                            return
                    self.newname_model.old_full_path = self.newname_model.new_full_path
                    self.newname_model.new_full_path = []

                elif self.newname_model.old_file_user_name[i] == '' and self.newname_model.new_file_user_name[i] == '':
                    self.show_warning('Writing a file name.')
                    self.window_all_clear()
                    return
            self.window_all_clear()
            self.show_warning('Rename is done.')

        elif not self.browse_count:
            self.show_warning('Push the browse button.')
            self.window_all_clear()
            return

    def window_all_clear(self):
        if self.action_count > 0:

            for i in range(self.action_count + 1):
                self.newname_model.old_text_widget[i].setText('')
                self.newname_model.new_text_widget[i].setText('')
                self.deleted_old_text_widget.append(self.newname_model.old_text_widget[i])
                self.deleted_new_text_widget.append(self.newname_model.new_text_widget[i])
                self.deleted_rename_hbox.append(self.newname_model.rename_hbox[i])
                self.deleted_rename_hwidget.append(self.newname_model.rename_hwidget[i])

            for i in range(self.action_count):
                self.newname_model.old_text_widget[i + 1].setParent(None)
                self.newname_model.new_text_widget[i + 1].setParent(None)
                self.newname_model.rename_hbox[i + 1].removeWidget(self.newname_model.old_text_widget[i + 1])
                self.newname_model.rename_hbox[i + 1].removeWidget(self.newname_model.new_text_widget[i + 1])
                self.newname_view.new_name_vbox_layout.takeAt(self.newname_view.new_name_vbox_layout.count() - 1)
        else:
            self.newname_model.old_text_widget[0].setText('')
            self.newname_model.new_text_widget[0].setText('')

            self.newname_model.old_text_widget = []
            self.newname_model.new_text_widget = []
            self.newname_model.rename_hbox = []
            self.newname_model.rename_hwidget = []

            self.newname_model.old_text_widget.insert(0, QLineEdit())
            self.newname_model.new_text_widget.insert(0, QLineEdit())
            self.newname_model.rename_hbox.insert(0, QHBoxLayout())
            self.newname_model.rename_hwidget.insert(0, QWidget())

        self.newname_model.old_full_path = []
        self.rename_view.line_edit.setText('')

        self.action_count = 0
        self.browse_count = False

        if self.file_list_dialog is not None:
            self.file_list_dialog.close()

    @staticmethod
    def show_warning(error_message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(f"{error_message}")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


def main():
    app = QApplication()
    controller = RenamePathController()
    window = QMainWindow()
    window.setCentralWidget(controller.rename_view)
    window.setWindowTitle("Renamer")
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
