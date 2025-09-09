import argparse
from src.mosaic import build_mosaic
from src.catalog import Catalog

# caldwell layout: CaldwellNumber : (col, row, col_span, row_span)
caldwell_layout = {
    33:  ( 2, 2, 2, 3),   # C33  Estern Veil Nebula
}

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Caldwell Catalog")
    parser.add_argument("--input-folder", default="caldwell_images")
    parser.add_argument("--output-file", default="caldwell_mosaic.jpg")
    parser.add_argument("--grid-cols", type=int, default=17)
    parser.add_argument("--thumb-size", type=int, default=300)
    parser.add_argument("--font-path", default="/System/Library/Fonts/HelveticaNeue.ttc")
    parser.add_argument("--font-size", type=int, default=32)
    parser.add_argument("--title-font-size", type=int, default=124)
    parser.add_argument("--padding", type=int, default=20)
    return parser.parse_args()

def main():
    args = parse_args()
    build_mosaic(args, caldwell_layout, Catalog.CALDWELL)

if __name__ == "__main__":
    main()
