class Errors:

    def __init__(self):
        self.list = []

    def report(self, msg):
        self.list.append(msg)
