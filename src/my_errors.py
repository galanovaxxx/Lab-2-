class DirectoryNotFoundError(Exception):
    def __init__(self, path, message=None):
        self.path = path
        if message is None:
            self.message = f"Директория не найдена: '{self.path}'"
        else:
            self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"DirectoryNotFoundError(path='{self.path}', message='{self.message}')"
