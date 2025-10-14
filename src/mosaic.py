# Ensure Pillow is installed
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    import sys
    print("Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont

from layout import compute_grid_rows, draw_grid
from drawing import draw_title, draw_progress
from utils import load_images, open_with_default_viewer
from parameters import Parameters

def get_mosaic_dimensions(params: Parameters) -> tuple[int, int]:
    grid_rows = compute_grid_rows(params.grid_cols, params.layout, params.catalog.count())
    thumb_size_scaled = params.get_thumb_size_scaled()
    padding_scaled = params.get_padding_scaled()
    mosaic_w = params.grid_cols * thumb_size_scaled + 2 * padding_scaled
    mosaic_h = grid_rows * thumb_size_scaled + 2 * padding_scaled
    return mosaic_w, mosaic_h

# Build the mosaic image based on the provided arguments, layout map, and catalog
def build_mosaic(params: Parameters) -> Image.Image:
    # Load individual images
    images: dict[int, Image.Image] = load_images(params.input_folder, params.catalog.prefix())

    # Create output image
    catalog_count = params.catalog.count()
    grid_rows = compute_grid_rows(params.grid_cols, params.layout, catalog_count)
    mosaic_w, mosaic_h = get_mosaic_dimensions(params)
    mosaic = Image.new("RGB", (mosaic_w, mosaic_h), "black")
    draw = ImageDraw.Draw(mosaic)

    # Load fonts
    font_size_scaled = params.get_font_size_scaled()
    title_font_size_scaled = params.get_title_font_size_scaled()
    try:
        font = ImageFont.truetype(params.font_path, font_size_scaled)
        title_font = ImageFont.truetype(params.font_path, title_font_size_scaled)
    except OSError:
        font = ImageFont.load_default(font_size_scaled)
        title_font = ImageFont.load_default(title_font_size_scaled)

    thumb_size_scaled = params.get_thumb_size_scaled()
    padding_scaled = params.get_padding_scaled()
    draw_title(draw, params.title, title_font, mosaic_w, thumb_size_scaled, padding_scaled)
    draw_grid(draw, mosaic, font, params, grid_rows, params.layout, images)

    # Show progress if not completed
    images_count = 0
    for num in images:
        found = False
        for obj in params.layout:
            if num in obj.numbers:
                images_count += obj.objects()
                found = True
                break
        if not found:
            images_count += 1

    if images_count < catalog_count:
        progress_text = f"Progress: {images_count} / {catalog_count}"
        draw_progress(draw, progress_text, font, params.grid_cols - 2, grid_rows - 1, padding_scaled, thumb_size_scaled)

    mosaic.save(params.output_file)
    print(f"Saved {params.output_file}")
    return mosaic
