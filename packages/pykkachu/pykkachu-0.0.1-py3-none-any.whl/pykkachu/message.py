class Message:
    def __init__(self, name):
        self.name = name

    def named(self, name):
        return name == self.name
