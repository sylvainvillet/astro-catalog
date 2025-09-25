from enum import Enum

# Define the catalogs with their prefixes, titles, and counts
class Catalog(Enum):
    MESSIER = ("M", "Messier Catalog", 110)
    CALDWELL = ("C", "Caldwell Catalog", 109)

    def prefix(self) -> str:
        return self.value[0]

    def title(self) -> str:
        return self.value[1]

    def count(self) -> int:
        return self.value[2]
    
    @staticmethod
    def from_prefix(prefix: str) -> "Catalog":
        for catalog in Catalog:
            if catalog.prefix() == prefix:
                return catalog
        return Catalog.MESSIER  # Default to MESSIER if not found
