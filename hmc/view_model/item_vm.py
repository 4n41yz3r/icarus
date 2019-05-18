from .name_normalizer import NameNormalizer
from .file_vm import FileViewModel

class ItemViewModel():
    def __init__(self, media_item, query):
        self.id = media_item.id
        self.files = ItemViewModel._get_files(media_item, query)
        self.title = ItemViewModel._normalize_title(media_item.title)
        self.kind = ItemViewModel._get_item_kind(self.files)
        self.hidden = 'hidden' in media_item.meta \
            and media_item.meta['hidden'] == True
    
    @staticmethod
    def _get_files(media_item, query):
        files = map(lambda f: FileViewModel(f), media_item.files)
        filtered_files = ItemViewModel._filter(files, query)
        return list(filtered_files)

    @staticmethod
    def _normalize_title(string):
        return NameNormalizer.normalize(string)

    @staticmethod
    def _get_item_kind(files):
        kinds = set(map(lambda f: f.kind, files))
        if 'audio' in kinds and 'video' in kinds:
            return 'mixed'
        if 'audio' in kinds:
             return 'audio'
        if 'video' in kinds:
            return 'video'
        return 'empty'

    @staticmethod
    def _filter(files, query):
        if 'kind' in query:
            kind = query['kind']
            files = filter(lambda i: i.kind == kind, files)
        return files
