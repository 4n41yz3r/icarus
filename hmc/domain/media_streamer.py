import mimetypes
from .base64 import Base64
from .range import RangedFileResponse

class MediaStreamer:
    """Media streaming service which supports partial content response"""

    def __init__(self, base64_file_path):
        path_bytes = Base64.decode(base64_file_path)
        self._path_bytes = path_bytes
        self._path_string = Base64.bytes_to_string(path_bytes)

    def respond(self, request):
        media_file = self._open_file()
        return self._create_ranged_response(request, media_file)

    def _open_file(self):
        return open(self._path_bytes, 'rb')

    def _create_ranged_response(self, request, media_file):
        content_type = self._guess_content_type()
        response = RangedFileResponse(request, media_file, content_type=content_type)
        self._add_content_disposition(response)
        return response

    def _guess_content_type(self):
        (content_type, _encoding) = mimetypes.guess_type(self._path_string)
        return content_type

    def _add_content_disposition(self, response):
        response['Content-Disposition'] = 'attachment; filename="%s"' % self._path_string
