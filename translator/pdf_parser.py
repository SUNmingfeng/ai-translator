from typing import Optional

import pdfplumber

from book.book import Book
from book.content import Content, ContentType, TableContent
from book.page import Page
from log.logger import LOG
from translator.exceptions import PageOutOfRangeException


class PDFParser:
    def __init__(self):
        pass
    def parse_pdf(self, pdf_file_path:str, pages:Optional[int]=None) -> Book:
        book = Book(pdf_file_path)

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text()
                tables = pdf_page.extract_tables()

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.content_add(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                # Handling tables
                if tables:
                    table = TableContent(tables)
                    page.content_add(table)
                    LOG.debug(f"[table]\n{table}")

                book.page_add(page)

        return book


