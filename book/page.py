from .content import Content


class Page:
    def __init__(self):
        self.contents = []

    def content_add(self, content: Content):
        self.contents.append(content)