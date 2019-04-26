"""Views"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .domain import Catalog
from .domain import MediaStreamer
from .view_model import CatalogViewModel


class CatalogView(View):
    def __init__(self):
        self.catalog = Catalog('/home/pi/downloads')

    def get(self, request):
        return render(request, 'index.html', {
            'catalog': CatalogViewModel(self.catalog, request.GET)
        })
    
    def post(self, request):
        command = request.POST.get('command', '')
        self.execute_command(command, request.POST)
        return self.get(request)
    
    def execute_command(self, command, params):
        if command == 'hide':
            self.catalog.hide_item(params.get('id'))
        elif command == 'unhide':
            self.catalog.unhide_item(params.get('id'))
        else:
            raise ValueError('Unrecognized command.')


class StreamView(View):
    def get(self, request, base64_file_path):
        streamer = MediaStreamer(base64_file_path)
        return streamer.respond(request)
