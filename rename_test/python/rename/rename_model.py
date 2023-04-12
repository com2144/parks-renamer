class RenamePathModel:
    def __init__(self):
        self.path = ''

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path


class RenameNewPathModel:
    def __init__(self):
        self.new_name = ''

    def set_new_name(self, new_name):
        self.new_name = new_name

    def get_new_name(self):
        return self.new_name
