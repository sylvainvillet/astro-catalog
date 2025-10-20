import flet as ft
from catalog import Catalog
from parameters import Parameters

PARAMETERS_KEY = "astro_catalog_parameters"
CATALOG_SELECTED_KEY = "astro_catalog_selected"

class Storage:
    def __init__(self, page: ft.Page):
        self.page = page

    def save_parameters(self, params: Parameters):
        self.page.client_storage.set(self.get_catalog_parameters_key(params.catalog), params.to_dict())

    def load_parameters(self) -> Parameters:
        catalog = self.load_catalog()
        key = self.get_catalog_parameters_key(catalog)
        if self.page.client_storage.contains_key(key):  # True if the key exists
            data = self.page.client_storage.get(key)
            return Parameters.from_dict(data if data is not None else {})
        else:
            return Parameters.default(catalog)

    def get_catalog_parameters_key(self, catalog: Catalog) -> str:
        return f"astro_catalog_parameters.{catalog.id()}"

    def save_catalog(self, catalog: Catalog):
        self.page.client_storage.set(CATALOG_SELECTED_KEY, catalog.id())

    def load_catalog(self) -> Catalog:
        if self.page.client_storage.contains_key(CATALOG_SELECTED_KEY):
            id = self.page.client_storage.get(CATALOG_SELECTED_KEY)
            if isinstance(id, str):
                return Catalog.from_id(id)
        return Catalog.MESSIER  # Default to MESSIER if not found

    def clear(self):
        self.page.client_storage.clear() 
