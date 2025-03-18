from typing import Optional

from click import prompt

from book.book import Book
from book.content import ContentType
from log.logger import LOG
from model.model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer


class PDFTranslator:
    def __init__(self, model:Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path:str, file_format:str='PDF', target_language:str='中文', output_file_path:str=None, pages:Optional[int]=None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)
        for page_index, page in enumerate(self.book.pages):
            for content_index, content in enumerate(page.contents):
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)
                translation, status = self.model.make_request(prompt)
                LOG.debug(translation)

                self.book.pages[page_index].contents[content_index].set_translation(translation,status)

            self.writer.save_translated_book(self.book, output_file_path, file_format)
