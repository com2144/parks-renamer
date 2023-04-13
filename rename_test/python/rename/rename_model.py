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
        self.new_names = []
        self.rename_button = []
