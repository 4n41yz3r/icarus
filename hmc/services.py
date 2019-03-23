"""Services"""

import os
import re
import base64
import mimetypes
from .range import RangedFileResponse


class CatalogViewModel():
    def __init__(self, catalog, query):
        items = map(lambda item: ItemViewModel(item, query), catalog.items)
        filtered_items = CatalogViewModel._filter(items, query)
        self.items = list(filtered_items)

    @staticmethod
    def _filter(items, query):
        if ('kind' in query):
            kind = query['kind']
            items = filter(lambda i: i.kind == kind or i.kind == 'mixed', items)
        return items


class ItemViewModel():
    def __init__(self, media_item, query):
        self.title = ItemViewModel._normalize_title(media_item.title)
        files = map(lambda media_file: FileViewModel(media_file), media_item.files)
        filtered_files = ItemViewModel._filter(files, query)
        self.files = list(filtered_files)
        file_kinds = list(set(map(lambda file: file.kind, self.files)))
        self.kind = ItemViewModel._get_item_kind(file_kinds)

    @staticmethod
    def _normalize_title(string):
        regex_filter = r'\W+|_|1080p|720p|540p|480p|mp4|h264|aac|bluray|web-dl|split scenes|rarbg'
        return re.sub(regex_filter, ' ', string, flags=re.IGNORECASE).strip()

    @staticmethod
    def _filter(files, query):
        if ('kind' in query):
            kind = query['kind']
            files = filter(lambda i: i.kind == kind, files)
        return files

    @staticmethod
    def _get_item_kind(kinds):
        if 'audio' in kinds and 'video' in kinds:
            return 'mixed'
        if 'audio' in kinds:
             return 'audio'
        if 'video' in kinds:
            return 'video'
        return 'empty'


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


class Catalog():
    """Catalog service used to load media items"""

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
        self.title = MediaItem._file_name(path)
        self.files = MediaItem._files(path)

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
    def _should_include(media):
        return media.is_media() and media.length() > 1024 * 1024


class MediaFile():
    """Single media file"""

    def __init__(self, path):
        self.path = path

    def source(self):
        path_bytes = self.path.encode('utf-8', 'surrogateescape')
        return Base64String.encode(path_bytes)

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
        return self._create_ranged_response(request, media_file)

    def _open_file(self):
        return open(self._path, 'rb')

    def _create_ranged_response(self, request, media_file):
        content_type = self._guess_content_type()
        response = RangedFileResponse(request, media_file, content_type=content_type)
        self._add_content_disposition(response)
        return response

    def _guess_content_type(self):
        (content_type, _encoding) = mimetypes.guess_type(self._string_path)
        return content_type

    def _add_content_disposition(self, response):
        response['Content-Disposition'] = 'attachment; filename="%s"' % self._string_path
