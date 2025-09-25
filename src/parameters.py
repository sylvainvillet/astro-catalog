import json
from dataclasses import dataclass, field, asdict
from catalog import Catalog
from special_objects import SpecialObject
import argparse

# Default parameters values who are multiplied by scale
THUMB_SIZE = 100
FONT_SIZE = 10
TITLE_FONT_SIZE = 42
PADDING = 5
LABEL_BOTTOM_SPACE = 7

@dataclass
class Parameters:
    input_folder: str = ""
    output_file: str = "messier_catalog.jpg"
    catalog: Catalog = Catalog.MESSIER
    layout: list[SpecialObject] = field(default_factory=list)
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

    @staticmethod
    def parameters_from_args(args: argparse.Namespace, catalog: Catalog, layout: list[SpecialObject]) -> 'Parameters':
        return Parameters(
            input_folder=args.input_folder,
            output_file=args.output_file,
            catalog=catalog,
            layout=layout,
            grid_cols=args.grid_cols,
            font_path=args.font_path,
        )

    def to_dict(self) -> dict[str, str | int | float | list[SpecialObject]]:
        d = asdict(self)
        d["catalog"] = self.catalog.prefix()
        #d["layout"] = [self.catalog.serialize_special_object(obj) for obj in self.layout]
        return d

    @classmethod
    def from_dict(cls, d: dict[str, str | int | float | list[SpecialObject]]) -> "Parameters":
        return cls(
            input_folder=str(d.get("input_folder", "")),
            output_file=str(d.get("output_file", "messier_catalog.jpg")),
            catalog=Catalog.from_prefix(str(d.get("catalog", Catalog.MESSIER.prefix()))),
            #layout=[SpecialObject(x) for x in d.get("layout", [])],
            grid_cols=int(d["grid_cols"]) if "grid_cols" in d and not isinstance(d["grid_cols"], list) else 17,
            scale=float(d["scale"]) if "scale" in d and not isinstance(d["scale"], list) else 3.0,
            font_path=str(d.get("font_path", "/System/Library/Fonts/HelveticaNeue.ttc")),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, data: str) -> "Parameters":
        return cls.from_dict(json.loads(data))