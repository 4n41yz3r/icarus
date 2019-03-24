import os
from .base64 import Base64

class MediaFile():
    """Single media file"""

    def __init__(self, path):
        self.path = path

    def source(self):
        path_bytes = Base64.string_to_bytes(self.path)
        return Base64.encode(path_bytes)

    def name(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    def length(self):
        with open(self.path, 'rb') as file:
            return file.seek(0, 2)

    def kind(self):
        ext = self.extension()
        if ext == 'mp4':
            return 'video'
        if ext == 'mp3':
            return 'audio'
        return 'unknown'

    def is_media(self):
        return self.kind() != 'unknown'

    def extension(self):
        return self.path[-3:].lower()
