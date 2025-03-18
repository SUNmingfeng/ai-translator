from enum import Enum, auto
from PIL import Image as PILImage
import pandas as pd

from log.logger import LOG


class ContentType(Enum):
    TEXT = auto()
    IMAGE = auto()
    TABLE = auto()

class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        return False

class TableContent(Content):
    def __init__(self, data, translation=None):
        df = pd.DataFrame(data)
        if len(df) != len(data) or len(data[0]) != len(df.columns):
            raise ValueError(f"Data and translation are not the same length")
        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            table_data = [row.strip().split() for row in translation.strip().split('\n')]
            translated_df = pd.DataFrame(table_data[1:], columns=table_data[0])
            self.translation = translated_df
            self.status = status
        except Exception as e:
            LOG.error(e)
            self.translation = None
            self.status = None

    def __str__(self):
        return self.original.to_string(header=False, index=False)

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        return self.original.to_string(header=False, index=False)
