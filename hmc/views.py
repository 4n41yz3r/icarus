"""Views"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .services import Catalog
from .services import CatalogViewModel
from .services import MediaStreamer

class CatalogView(View):
    def get(self, request):
        catalog = Catalog('/home/pi/downloads')
        return render(request, 'index.html', {
            'catalog': CatalogViewModel(catalog, request.GET)
        })


class StreamView(View):
    def get(self, request, base64_file_path):
        streamer = MediaStreamer(base64_file_path)
        return streamer.respond(request)
