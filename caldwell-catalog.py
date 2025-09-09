import argparse
from src.mosaic import build_mosaic
from src.catalog import Catalog

# Caldwell layout: CaldwellNumber : (col, row, col_span, row_span)
caldwell_layout = {
    20: ( 1, 1, 3, 2),    # C20 North America Nebula
    33: (14, 1, 2, 3),    # C33 Veil Nebula 
    68: ( 7, 2, 2, 2),    # C68 Helix Nebula 
    70: ( 2, 4, 3, 2),    # C70 NGC 300
    71: ( 9, 5, 4, 2),    # C71 Large Magellanic Cloud
    72: ( 0, 7, 3, 2),    # C72 Small Magellanic Cloud
    99: (14, 6, 3, 2),    # C99 Coalsack Nebula
}

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Caldwell Catalog")
    parser.add_argument("--input-folder", default="caldwell_images")
    parser.add_argument("--output-file", default="caldwell_mosaic.jpg")
    parser.add_argument("--title", default=Catalog.CALDWELL.title())
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
