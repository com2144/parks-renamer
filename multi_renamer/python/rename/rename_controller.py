from PySide2.QtWidgets import *
from rename.rename_model import RenamePathModel
from rename.rename_view import RenamePathView
from rename.rename_model import RenameNewPathModel
from rename.rename_view import RenameNewPathView
import os
import platform


class RenamePathController:
    def __init__(self):
        self.rename_model = RenamePathModel()
        self.rename_view = RenamePathView()
        self.newname_model = RenameNewPathModel()
        self.newname_view = RenameNewPathView()
        self.dir_path = self.rename_model.path
        self.action_count = 0
        self.browse_action_count = 0

        self.deleted_old_text_widget = []
        self.deleted_new_text_widget = []
        self.deleted_rename_hbox = []
        self.deleted_rename_hwidget = []

        self.closed = 0

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
        if hasattr(self, 'file_list_dialog'):
            self.file_list_dialog.close()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        self.dir_path = QFileDialog.getExistingDirectory(None, "Select Directory", "", options=options)

        if os.path.exists(self.dir_path):
            self.set_file_path(self.dir_path)
            self.rename_view.line_edit.setText(self.dir_path)
            self.dir_path = self.dir_path + '/'
            self.newname_model.old_path.append(self.dir_path)
        if self.dir_path:
            self.show_files_in_directory(self.dir_path)

    def show_files_in_directory(self, directory):
        file_list = os.listdir(directory)

        file_list_dialog = QDialog()
        file_list_dialog.setWindowTitle("Files in Directory")

        list_widget = QListWidget(file_list_dialog)
        for file in file_list:
            file_name, _ = os.path.splitext(file)
            list_widget.addItem(file_name)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(list_widget)
        file_list_dialog.setLayout(dialog_layout)

        file_list_dialog.setModal(False)

        self.file_list_dialog = file_list_dialog

        file_list_dialog.finished.connect(lambda: delattr(self, 'file_list_dialog'))

        file_list_dialog.show()
        file_list_dialog.exec_()

    def set_file_path(self, file_path):
        file_list = os.listdir(file_path)
        self.newname_model.old_file_name.append(file_list)

        print("aaa", file_list)

        for i in file_list:
            file_name, file_ext = os.path.splitext(i)
            self.newname_model.old_file_ext.append(file_ext)
            self.newname_model.old_path.append(file_path + '/' + i)

        self.browse_action_count += 1

        # for i in range(self.browse_action_count):
        #     second_old_file_name.insert(i, self.newname_model.old_file_name)
        # print("aaa", second_old_file_name)

        # if self.action_count == 0 and not self.newname_model.old_text_widget[0].text():
        #     self.newname_model.old_text_widget[0].setText(file_read_name)
        #     return
        #
        # if self.action_count == 0 and self.newname_model.old_text_widget[0].text():
        #     self.newname_model.old_text_widget[0].clear()
        #     self.newname_model.old_text_widget[0].setText(file_read_name)
        #
        # if self.action_count > 0 and not self.newname_model.old_text_widget[0].text():
        #     self.newname_model.old_text_widget[0].setText(file_read_name)
        #     return
        #
        # for index, widget in enumerate(self.newname_model.old_text_widget[1:], start=1):
        #     if not widget.text():
        #         widget.setText(file_read_name)
        #         break

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
                self.newname_model.old_path.pop()
                self.newname_model.old_file_ext.pop()
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

        # for new_text in self.newname_model.new_text_widget:
        #     self.newname_model.new_file_name.append(new_text.text())
        #
        # for index, old_text in enumerate(self.newname_model.old_text_widget):
        #     if old_text.text() and self.newname_model.new_file_name[index] and platform.system() != 'Windows':
        #         os.rename(self.newname_model.old_path[index], os.path.join(self.rename_model.old_file_dir_path[index],
        #                                                                    self.newname_model.new_file_name[index] +
        #                                                                    self.newname_model.file_ext[index]))
        #     elif old_text.text() and self.newname_model.new_file_name[index] and platform.system() == 'Windows':
        #         old_path = self.newname_model.old_path[index]
        #         old_path = old_path.replace('/', '\\')
        #         new_path = os.path.join(self.rename_model.old_file_dir_path[index],
        #                                 self.newname_model.new_file_name[index] + self.newname_model.file_ext[index])
        #         new_path = new_path.replace('/', '\\')
        #         os.rename(old_path, new_path)
        #     else:
        #         pass

        if self.action_count > 0:
            for i in range(self.action_count + 1):
                self.deleted_old_text_widget.append(self.newname_model.old_text_widget[i])
                self.deleted_new_text_widget.append(self.newname_model.new_text_widget[i])
                self.deleted_rename_hbox.append(self.newname_model.rename_hbox[i])
                self.deleted_rename_hwidget.append(self.newname_model.rename_hwidget[i])
                self.newname_model.old_text_widget[i].clear()
                self.newname_model.new_text_widget[i].clear()

            for i in range(self.action_count):
                self.newname_model.old_text_widget[i + 1].setParent(None)
                self.newname_model.new_text_widget[i + 1].setParent(None)
                self.newname_model.rename_hbox[i + 1].removeWidget(self.newname_model.old_text_widget[i + 1])
                self.newname_model.rename_hbox[i + 1].removeWidget(self.newname_model.new_text_widget[i + 1])
                self.newname_view.new_name_vbox_layout.takeAt(self.newname_view.new_name_vbox_layout.count() - 1)

            self.newname_model.old_text_widget.clear()
            self.newname_model.new_text_widget.clear()
            self.newname_model.rename_hbox.clear()
            self.newname_model.rename_hwidget.clear()

            self.action_count = 0

            if hasattr(self, 'file_list_dialog'):
                self.file_list_dialog.close()


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
