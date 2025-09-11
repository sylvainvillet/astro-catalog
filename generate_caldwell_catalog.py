import argparse
from user_settings import caldwell_layout
from src.mosaic import build_mosaic
from src.catalog import Catalog

def parse_args():
    parser = argparse.ArgumentParser(description="Generate Caldwell Catalog")
    parser.add_argument("--input-folder", default="caldwell_images")
    parser.add_argument("--output-file", default="caldwell_catalog.jpg")
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
