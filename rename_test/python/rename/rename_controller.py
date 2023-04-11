from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout
from rename.rename_model import RenameModel
from rename.rename_veiw import RenameView

class RenameController:
    def __init__(self, model, view):
        self.path_model = model
        self.path_view = view

    def on_text_changed(self,text):
        self.path_model.set_path(text)

    def get_text(self):
        return self.path_model.get_path()

    def on_browse_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self.path_view, "Select a file", "", "All Files (*);;Python Files (*.py)",
                                                   options=options)

        if file_path:
            self.path_model.set_path(file_path)
            # self.path_view.path_update()

def main():
    app = QApplication()
    window = QWidget()
    model = RenameModel()
    controller = RenameController(model, None)
    view = RenameView(controller)
    controller.view = view
    view.controller = controller

    window.setLayout(view.main_layout)
    window.show()

    app.exec_()

if __name__ == '__main__':
    main()