import re

class FileViewModel():
    def __init__(self, media_file):
        self.name = FileViewModel._normalize_name(media_file.name())
        self.source = media_file.source()
        self.kind = media_file.kind()

    @staticmethod
    def _normalize_name(string):
        string = re.sub(r'-', ' - ', string)
        string = re.sub(r'\.[^\. ]+$|[ _\.]+', ' ', string.lower()).strip()
        return string.encode('utf-8', 'surrogateescape') #errors='replace'
