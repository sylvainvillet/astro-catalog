# Ensure Pillow is installed
try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    import subprocess
    import sys
    print("Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont, ImageOps

from typing import Dict, Any
from argparse import Namespace
from src.layout import compute_grid_rows, draw_grid
from src.drawing import draw_title, draw_progress
from src.utils import load_images, open_with_default_viewer
from src.catalog import Catalog

__version__ = "1.0.1"

def build_mosaic(args: Namespace, layout_map: dict[int, tuple[int, int, int, int]], catalog: Catalog):
    print(f"Astro Catalog v{__version__}, created by Sylvain Villet")

    # Load individual images
    images = load_images(args.input_folder, args.thumb_size, catalog.prefix())

    # Create output image
    catalog_count = catalog.count()
    grid_rows = compute_grid_rows(args.grid_cols, layout_map, catalog_count)
    mosaic_w = args.grid_cols * args.thumb_size + 2 * args.padding
    mosaic_h = grid_rows * args.thumb_size + 2 * args.padding
    mosaic = Image.new("RGB", (mosaic_w, mosaic_h), "black")
    draw = ImageDraw.Draw(mosaic)

    try:
        font = ImageFont.truetype(args.font_path, args.font_size)
        title_font = ImageFont.truetype(args.font_path, args.title_font_size)
    except OSError:
        font = ImageFont.load_default(args.font_size)
        title_font = ImageFont.load_default(args.title_font_size)

    draw_title(draw, args.title, title_font, mosaic_w, args.thumb_size, args.padding)
    draw_grid(draw, mosaic, font, args, grid_rows, layout_map, images, catalog)

    # Show progress if not completed
    images_count = len(images)
    if images_count < catalog_count:
        progress_text = f"Progress: {images_count} / {catalog_count}"
        draw_progress(draw, progress_text, font, args.grid_cols - 2, grid_rows - 1, args.padding, args.thumb_size)

    mosaic.save(args.output_file)
    print(f"Saved {args.output_file}")
    open_with_default_viewer(args.output_file)
