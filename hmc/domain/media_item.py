import os
import json
import hashlib
from .media_file import MediaFile
from .base64 import Base64

class MediaItem():
    """Single item item in the catalog"""

    def __init__(self, path):
        self.path = path
        self.id = self._get_id()
        self.title = self._file_name()
        self.files = self._load_files()
        self.meta = self._load_meta()

    def hide(self):
        self.meta['hidden'] = True
        self._save_meta()
    
    def unhide(self):
        self.meta['hidden'] = False
        self._save_meta()

    def _get_id(self):
        return hashlib.md5(Base64.string_to_bytes(self.path)).hexdigest()

    def _file_name(self):
        return os.path.basename(self.path)

    def _load_files(self):
        if os.path.isdir(self.path):
            for (root, _folders, files) in os.walk(self.path):
                for file in files:
                    file_path = os.path.join(root, file)
                    media = MediaFile(file_path)
                    if MediaItem._should_include(media):
                        yield media
        else:
            media = MediaFile(self.path)
            yield media

    def _load_meta(self):
        meta_path = '{0}/meta.json'.format(self.path)
        if os.path.exists(meta_path):
            with open(meta_path, "r") as meta_file:
                serialized_meta = meta_file.read()
                return json.loads(serialized_meta)
        return dict()

    def _save_meta(self):
        meta_path = '{0}/meta.json'.format(self.path)
        with open(meta_path, "w") as meta_file:
            serialized_meta = json.dumps(self.meta)
            meta_file.write(serialized_meta)

    @staticmethod
    def _should_include(media):
        return media.is_media() and media.length() > 1024 * 1024
