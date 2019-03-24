import os
import json
from .media_file import MediaFile

class MediaItem():
    """Single item item in the catalog"""

    def __init__(self, path):
        self.title = MediaItem._file_name(path)
        self.files = MediaItem._files(path)
        self.meta = MediaItem._metadata(path)

    @staticmethod
    def _file_name(path):
        return os.path.basename(path)

    @staticmethod
    def _files(path):
        if os.path.isdir(path):
            for (root, _folders, files) in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    media = MediaFile(file_path)
                    if MediaItem._should_include(media):
                        yield media
        else:
            media = MediaFile(path)
            yield media

    @staticmethod
    def _metadata(path):
        meta_path = '{0}/meta.json'.format(path)
        if os.path.exists(meta_path):
            with open(meta_path, "r") as meta_file:
                serialized_meta = meta_file.read()
                return json.loads(serialized_meta)
        return dict()

    @staticmethod
    def _should_include(media):
        return media.is_media() and media.length() > 1024 * 1024
