class RenamePathModel:
    def __init__(self):
        self.path = ''

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path


class RenameNewPathModel:
    def __init__(self):
        self.old_names = []
        self.old_text_widget = []
        # self.new_names = []
        self.new_text_widget = []
        self.rename_hbox = []
        self.rename_hwidget = []


    def set_new_name(self, file_name):
        self.old_names.append(file_name)


