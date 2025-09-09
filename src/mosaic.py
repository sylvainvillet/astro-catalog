from PIL import Image, ImageDraw, ImageFont, ImageOps
from src.layout import compute_grid_rows, draw_grid
from src.drawing import draw_title, draw_progress
from src.utils import load_images, open_with_default_viewer
from src.catalog import Catalog

def build_mosaic(args, layout_map, catalog):
    catalog_count = catalog.count()
    images = load_images(args.input_folder, args.thumb_size, catalog.prefix())

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

    draw_title(draw, catalog.title(), title_font, mosaic_w, args.thumb_size, args.padding)
    draw_grid(draw, mosaic, font, args, grid_rows, layout_map, images, catalog)

    images_count = len(images)
    if images_count < catalog_count:
        progress_text = f"{images_count} / {catalog_count}"
        draw_progress(draw, progress_text, font, args.grid_cols - 1, grid_rows - 1, args.padding, args.thumb_size)

    mosaic.save(args.output_file, format="JPEG", quality=100, optimize=True)
    print(f"Saved {args.output_file}")
    open_with_default_viewer(args.output_file)
