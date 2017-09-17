"""Views"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .services import Catalog
from .services import Base64String
from .services import MediaStreamer

class CatalogView(View):
    def get(self, request):
        cat = Catalog('/home/pi/downloads')
        return render(request, 'index.html', {
            'items': cat.items
        })


class StreamView(View):
    def get(self, request, base64_media_path):
        path = Base64String.decode(base64_media_path)
        streamer = MediaStreamer(path)
        return streamer.respond(request)