import copy
from enum import Enum
import json
from dataclasses import dataclass, field, asdict
from catalog import Catalog
from special_objects import SpecialObject

# Default parameters values who are multiplied by scale
THUMB_SIZE = 100
FONT_SIZE = 10
TITLE_FONT_SIZE = 42
PADDING = 5
LABEL_BOTTOM_SPACE = 7

# Default layouts for Messier and Caldwell catalogs
default_messier_layout: list[SpecialObject] = [
    SpecialObject(numbers=[8, 20],       x=3, y=2, width=2, height=3),   # Lagoon Nebula
    SpecialObject(numbers=[16],          x=15, y=2, width=2, height=2),  # Eagle Nebula
    SpecialObject(numbers=[31, 32, 110], x=8, y=2, width=4, height=2),   # Andromeda
    SpecialObject(numbers=[33],          x=2, y=6, width=3, height=2),   # Triangulum Galaxy
    SpecialObject(numbers=[42, 43],      x=7, y=5, width=2, height=3),   # Orion Nebula
    SpecialObject(numbers=[45],          x=14, y=5, width=2, height=2),  # Pleiades
]

default_caldwell_layout: list[SpecialObject] = [
    SpecialObject(numbers=[20], x=2, y=1, width=3, height=2),   # North America Nebula
    SpecialObject(numbers=[33], x=12, y=2, width=2, height=3),  # Veil Nebula
    SpecialObject(numbers=[34], x=14, y=2, width=2, height=3),  # Veil Nebula
    SpecialObject(numbers=[68], x=8, y=2, width=2, height=2),   # Helix Nebula
    SpecialObject(numbers=[70], x=3, y=4, width=3, height=2),   # NGC 300
    SpecialObject(numbers=[71], x=8, y=7, width=4, height=2),   # Large Magellanic Cloud
    SpecialObject(numbers=[72], x=1, y=7, width=3, height=2),   # Small Magellanic Cloud
    SpecialObject(numbers=[99], x=15, y=6, width=3, height=2),  # Coalsack Nebula
]

class LayoutMode(Enum):
    BASIC = "Basic"
    ENHANCED = "Enhanced"

@dataclass
class Parameters:
    input_folder: str = ""
    output_file: str = ""
    title: str = ""
    catalog: Catalog = Catalog.MESSIER
    layout: list[SpecialObject] = field(default_factory=list)
    layout_mode: LayoutMode = LayoutMode.ENHANCED
    grid_cols: int = 17
    scale: float = 2.0
    font_path: str = "/System/Library/Fonts/HelveticaNeue.ttc"

    def get_thumb_size_scaled(self) -> int:
        return int(THUMB_SIZE * self.scale)
    
    def get_font_size_scaled(self) -> int:
        return int(FONT_SIZE * self.scale)

    def get_title_font_size_scaled(self) -> int:
        return int(TITLE_FONT_SIZE * self.scale)

    def get_padding_scaled(self) -> int:
        return int(PADDING * self.scale)
    
    def get_label_bottom_space_scaled(self) -> int:
        return int(LABEL_BOTTOM_SPACE * self.scale)

    def get_special_objects(self) -> list[SpecialObject]:
        if self.layout_mode == LayoutMode.BASIC:
            return []
        return self.layout

    @classmethod
    def messier_default(cls) -> "Parameters":
        return cls(
            output_file="messier_catalog.png",
            title=Catalog.MESSIER.title(),
            layout=copy.deepcopy(default_messier_layout),
        )
    
    @classmethod
    def caldwell_default(cls) -> "Parameters":
        return cls(
            output_file="caldwell_catalog.png",
            title=Catalog.CALDWELL.title(),
            catalog=Catalog.CALDWELL,
            layout=copy.deepcopy(default_caldwell_layout)
        )
    
    @classmethod
    def default(cls, catalog: Catalog) -> "Parameters":
        if catalog == Catalog.MESSIER:
            return cls.messier_default()
        else:
            return cls.caldwell_default()
    
    def to_dict(self) -> dict[str, str | int | float | list[SpecialObject]]:
        d = asdict(self)
        d["catalog"] = self.catalog.id()
        d["layout"] = [obj.to_dict() for obj in self.layout]
        d["layout_mode"] = self.layout_mode.value
        return d

    @classmethod
    def from_dict(cls, d: dict[str, str | int | float | list[SpecialObject]]) -> "Parameters":
        return cls(
            input_folder=str(d.get("input_folder", "")),
            output_file=str(d.get("output_file", "messier_catalog.jpg")),
            title=str(d.get("title", "")),
            catalog=Catalog.from_id(str(d.get("catalog", Catalog.MESSIER.id()))),
            layout=[
                SpecialObject.from_dict(obj) for obj in d.get("layout", []) if isinstance(obj, dict)
            ],
            layout_mode=LayoutMode(d.get("layout_mode", LayoutMode.ENHANCED.value)),
            grid_cols=int(d["grid_cols"]) if "grid_cols" in d and not isinstance(d["grid_cols"], list) else 17,
            scale=float(d["scale"]) if "scale" in d and not isinstance(d["scale"], list) else 3.0,
            font_path=str(d.get("font_path", "/System/Library/Fonts/HelveticaNeue.ttc")),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data: str) -> "Parameters":
        return cls.from_dict(json.loads(data))