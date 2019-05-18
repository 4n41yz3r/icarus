import re
from .name_normalizer import NameNormalizer

class FileViewModel():
    def __init__(self, media_file):
        self.name = FileViewModel._normalize_name(media_file.name())
        self.source = media_file.source()
        self.kind = media_file.kind()

    @staticmethod
    def _normalize_name(string):
        return NameNormalizer.normalize_file(string)
