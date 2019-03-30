import os
from .media_item import MediaItem

class Catalog():
    """Catalog service used to load media items"""

    def __init__(self, path):
        self.path = path
        self.items = list(self._load_items())

    def hide_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                item.hide()
                break

    def _load_items(self):
        paths = self._list_folder_content()
        return self._project_into_items(paths)

    def _list_folder_content(self):
        (root, folders, files) = next(os.walk(self.path))
        for file in sorted(files):
            yield os.path.join(root, file)
        for folder in sorted(folders):
            yield os.path.join(root, folder)

    def _project_into_items(self, path_list):
        for path in path_list:
            yield MediaItem(path)
