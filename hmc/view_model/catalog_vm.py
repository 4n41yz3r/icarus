from .item_vm import ItemViewModel

class CatalogViewModel():
    def __init__(self, catalog, query):
        self.items = CatalogViewModel._get_items(catalog, query)

    @staticmethod
    def _get_items(catalog, query):
        items = map(lambda item: ItemViewModel(item, query), catalog.items)
        filtered_items = CatalogViewModel._filter(items, query)
        return list(filtered_items)

    @staticmethod
    def _filter(items, query):
        if 'hidden' not in query:
            items = filter(lambda i: not i.hidden, items)
        if 'kind' in query:
            kind = query['kind']
            items = filter(lambda i: i.kind == kind or i.kind == 'mixed', items)
        return items
