import argparse
from src.mosaic import build_mosaic
from src.catalog import Catalog

# Messier layout: MessierNumber : (col, row, col_span, row_span)
messier_layout = {
    8:  ( 2, 1, 2, 2),   # M8  Lagoon Nebula
    16: (14, 1, 2, 2),   # M16 Eagle Nebula
    31: ( 7, 2, 4, 2),   # M31 Andromeda
    33: ( 1, 4, 3, 2),   # M33 Triangulum Galaxy
    42: ( 5, 5, 2, 2),   # M42 Orion Nebula
    45: (13, 4, 2, 2),   # M45 Pleiades
    # Others default to auto-placement or smaller slots if not listed
}

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Messier Catalog")
    parser.add_argument("--input-folder", default="messier_images")
    parser.add_argument("--output-file", default="messier_mosaic.jpg")
    parser.add_argument("--grid-cols", type=int, default=17)
    parser.add_argument("--thumb-size", type=int, default=300)
    parser.add_argument("--font-path", default="/System/Library/Fonts/HelveticaNeue.ttc")
    parser.add_argument("--font-size", type=int, default=32)
    parser.add_argument("--title-font-size", type=int, default=124)
    parser.add_argument("--padding", type=int, default=20)
    return parser.parse_args()

def main():
    args = parse_args()
    build_mosaic(args, messier_layout, Catalog.MESSIER)

if __name__ == "__main__":
    main()
