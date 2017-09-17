"""Services"""

import os
import re
import base64
import mimetypes
from .range import RangedFileResponse

class Catalog():
    """Catalog service used to load video items"""

    def __init__(self, path):
        self._path = path
        self.items = list(self._load_items())

    def _load_items(self):
        paths = self._list_folder_content()
        return self._project_into_items(paths)

    def _list_folder_content(self):
        (root, folders, files) = next(os.walk(self._path))
        for file in sorted(files):
            yield os.path.join(root, file)
        for folder in sorted(folders):
            yield os.path.join(root, folder)

    def _project_into_items(self, path_list):
        for path in path_list:
            yield MediaItem(path)


class MediaItem():
    """Single item item in the catalog"""

    def __init__(self, path):
        self.title = MediaItem._normalize(MediaItem._get_file_name(path))
        self.files = MediaItem._get_files(path)

    @staticmethod
    def _get_file_name(path):
        return os.path.basename(path)

    @staticmethod
    def _get_files(path):
        if os.path.isdir(path):
            for (root, _folders, files) in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    media = MediaFile(file_path)
                    if MediaItem._should_display_media(media):
                        yield MediaViewModel(media)
        else:
            media = MediaFile(path)
            yield MediaViewModel(media)

    @staticmethod
    def _should_display_media(media):
        return media.is_media() and media.length() > 1024 * 1024

    @staticmethod
    def _normalize(string):
        regex_filter = r'\W+|_|1080p|720p|540p|480p|mp4|h264|aac|bluray|web-dl|split scenes|rarbg'
        return re.sub(regex_filter, ' ', string, flags=re.IGNORECASE).strip()


class MediaFile():
    """Single media file"""

    def __init__(self, path):
        self.path = path

    def source(self):
        bytes_path = self.path.encode('utf-8', 'surrogateescape')
        return Base64String.encode(bytes_path)

    def kind(self):
        ext = self.extension()
        if ext == 'mp4':
            return 'video'
        if ext == 'mp3':
            return 'audio'
        return 'unknown'

    def file_name(self):
        return os.path.basename(self.path)

    def length(self):
        with open(self.path, 'rb') as file:
            length = file.seek(0, 2)
            return length

    def is_media(self):
        ext = self.extension()
        return ext == 'mp4' or ext == 'mp3'

    def extension(self):
        return self.path[-3:].lower()


class MediaViewModel():
    def __init__(self, media):
        self.name = MediaViewModel._normalize_name(media.file_name())
        self.source = media.source()
        self.kind = media.kind()

    @staticmethod
    def _normalize_name(string):
        string = re.sub(r'-', ' - ', string)
        string = re.sub(r'\.[^\. ]+$|[ _\.]+', ' ', string.lower()).strip()
        return string.encode('utf-8', 'surrogateescape') #errors='replace'


class Base64String:
    """Base64 string encoding helper"""

    @staticmethod
    def encode(input_bytes):
        """Encode bytes to base64 string"""
        encoded_bytes = base64.urlsafe_b64encode(input_bytes)
        return encoded_bytes.decode('utf-8')

    @staticmethod
    def decode(input_str):
        """Decode base64 string to bytes"""
        bytes_string = input_str.encode('utf-8')
        decoded_bytes = base64.urlsafe_b64decode(bytes_string)
        return decoded_bytes


class MediaStreamer:
    """Media streaming service which supports partial content response"""

    def __init__(self, path):
        self._path = path
        self._string_path = path.decode('utf8', 'surrogateescape')

    def respond(self, request):
        media_file = self._open_file()
        content_type = self._guess_content_type()
        return self._create_ranged_response(request, media_file, content_type)

    def _open_file(self):
        return open(self._path, 'rb')

    def _guess_content_type(self):
        (content_type, _encoding) = mimetypes.guess_type(self._string_path)
        return content_type

    def _create_ranged_response(self, request, media_file, content_type):
        response = RangedFileResponse(request, media_file, content_type=content_type)
        self._add_content_disposition(response)
        return response

    def _add_content_disposition(self, response):
        response['Content-Disposition'] = 'attachment; filename="%s"' % self._string_path