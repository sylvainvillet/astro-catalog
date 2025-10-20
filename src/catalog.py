from enum import Enum

# Define the catalogs with their prefixes, titles, and counts
class Catalog(Enum):
    MESSIER = ("messier", "M", "Messier Catalog", 110)
    CALDWELL = ("caldwell", "C", "Caldwell Catalog", 109)

    def id(self) -> str:
        return self.value[0]

    def prefix(self) -> str:
        return self.value[1]

    def title(self) -> str:
        return self.value[2]

    def count(self) -> int:
        return self.value[3]
    
    @staticmethod
    def from_id(id: str) -> "Catalog":
        for catalog in Catalog:
            if catalog.id() == id:
                return catalog
        return Catalog.MESSIER  # Default to MESSIER if not found
