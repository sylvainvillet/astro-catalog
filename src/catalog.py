from enum import Enum

class Catalog(Enum):
    MESSIER = ("M", "Messier Catalog", 110)
    CALDWELL = ("C", "Caldwell Catalog", 109)

    def prefix(self) -> str:
        return self.value[0]

    def title(self) -> str:
        return self.value[1]

    def count(self) -> int:
        return self.value[2]
