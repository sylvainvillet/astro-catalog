from dataclasses import dataclass, field
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
    scale: float = 1.0
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