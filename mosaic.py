import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageOps


# --- SETTINGS ---
input_folder = "messier_images"   # where your M_xx_ files are
output_file = "messier_mosaic.jpg"
grid_cols = 16
thumb_size = (300, 300)   # size of each Messier thumbnail
font_path = "/System/Library/Fonts/HelveticaNeue.ttc"
font_size = 32
title_font_size = 124
padding = 5  # space inside each slot for the image
border_padding = 20  # space around the whole mosaic

# Messier layout: MessierNumber : (col, row, col_span, row_span)
layout_map = {
    8:  ( 2, 1, 2, 2),   # M8  Lagoon Nebula
    16: (13, 1, 2, 2),   # M16 Eagle Nebula
    31: ( 7, 2, 4, 2),   # M31 Andromeda
    33: ( 5, 5, 2, 2),   # M33 Triangulum Galaxy
    42: (12, 5, 2, 2),   # M42 Orion Nebula
    45: ( 1, 4, 2, 2),   # M45 Pleiades
    # Others default to auto-placement or smaller slots if not listed
}

def compute_grid_rows(grid_cols, layout_map, total=110):
    special_cells = sum(col_span * row_span for (_, _, col_span, row_span) in layout_map.values())
    normal_cells = total - len(layout_map)
    total_cells = special_cells + normal_cells
    # round up to full rows
    return -(-total_cells // grid_cols) + 1  # ceil division

grid_rows = compute_grid_rows(grid_cols, layout_map)

# --- LOAD IMAGES ---
pattern = re.compile(r"M(\d+)_")
images = {}
for fname in os.listdir(input_folder):
    match = pattern.match(fname)
    if match:
        num = int(match.group(1))
        path = os.path.join(input_folder, fname)
        try:
            img = Image.open(path).convert("RGB")
            img = ImageOps.fit(img, thumb_size, Image.LANCZOS, centering=(0.5, 0.5))
            images[num] = img
        except Exception as e:
            print(f"Error loading {fname}: {e}")

# --- PREPARE MOSAIC ---
mosaic_w = grid_cols * thumb_size[0] + 2 * border_padding
mosaic_h = grid_rows * thumb_size[1] + 2 * border_padding
mosaic = Image.new("RGB", (mosaic_w, mosaic_h), "black")

draw = ImageDraw.Draw(mosaic)
try:
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(font_path, title_font_size)
except OSError:
    font = ImageFont.load_default(font_size)
    title_font = ImageFont.load_default(title_font_size)

# --- HELPER FUNCTION ---

def draw_title(text="Messier Catalog"):
    """Draw title centered across the top row."""
    # Full width of the mosaic
    width = mosaic_w
    # Reserve height for the title
    title_row_height = thumb_size[1]

    # Compute text size
    bbox = draw.textbbox((0, 0), text, font=title_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Center text horizontally and vertically in the row
    text_x = (width - tw) // 2
    text_y = (title_row_height - th) // 2

    # Optional: background rectangle
    draw.rectangle([0, 0, width, title_row_height], fill="black")

    draw.text((text_x, text_y), text, fill="white", font=title_font)


def place_messier(num, col, row, col_span=1, row_span=1):
    """Place a Messier image or placeholder at the given slot and mark occupied cells."""
    slot_w = col_span * thumb_size[0]
    slot_h = row_span * thumb_size[1]
    x = col * thumb_size[0] + border_padding
    y = row * thumb_size[1] + border_padding

    # Draw border first
    draw.rectangle([x, y, x + slot_w - 1, y + slot_h - 1], outline="gray", width=2)

    # Place image or placeholder
    if num in images:
        img = ImageOps.fit(
            images[num],
            (slot_w - 2 * padding, slot_h - 2 * padding),
            Image.LANCZOS,
            centering=(0.5, 0.5)
        )
        mosaic.paste(img, (x + padding, y + padding))

        # Draw the name on the image (centered at the bottom)
        name_text = f"M{num}"
        bbox = draw.textbbox((0, 0), name_text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        text_x = x + (slot_w - tw) // 2
        text_y = y + slot_h - th - 20  # 5px padding from bottom
        draw.text((text_x, text_y), name_text, fill="white", font=font)

    else:
        text = f"M{num}"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(
            (x + (slot_w - tw) // 2, y + (slot_h - th) // 2),
            text,
            fill="white",
            font=font
        )

    # Mark cells as occupied
    for r in range(row, row + row_span):
        for c in range(col, col + col_span):
            if r < grid_rows and c < grid_cols:
                occupied[r][c] = True

def draw_progress_image_count():
    """Draw bottom-right 1x1 slot with number of loaded images."""
    col = grid_cols - 1  # last column
    row = grid_rows - 1  # last row
    slot_w = 1 * thumb_size[0]
    slot_h = 1 * thumb_size[1]
    x = col * thumb_size[0] + border_padding
    y = row * thumb_size[1] + border_padding

    text = f"{len(images)} / 110"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        (x + (slot_w - tw) // 2, y + (slot_h - th) // 2),
        text,
        fill="white",
        font=font
    )

# --- MESSIER PLACEMENT LOOP ---
# Initialize occupancy grid
occupied = [[False] * grid_cols for _ in range(grid_rows)]

# Reserve the first row for the title
for c in range(grid_cols):
    occupied[0][c] = True

draw_title()

# --- PLACE LARGE MESSIERS FIRST ---
for num, (col, row, col_span, row_span) in layout_map.items():
    place_messier(num, col, row+1, col_span, row_span) # Row +1 because title is in 1st row

# --- PLACE REMAINING SMALL MESSIERS ---
for i in range(110):
    num = i + 1
    if num in layout_map:
        continue  # already placed

    # Find first free 1x1 slot
    placed = False
    for r in range(grid_rows):
        for c in range(grid_cols):
            if not occupied[r][c]:
                place_messier(num, c, r)
                placed = True
                break
        if placed:
            break

if len(images) < 110:
    draw_progress_image_count()

# Save result
mosaic.save(output_file)
print(f"Mosaic saved as {output_file}")
