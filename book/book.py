from .page import Page


class Book:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.pages = []

    def page_add(self, page: Page):
        self.pages.append(page)