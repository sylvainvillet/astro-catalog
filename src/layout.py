from PIL import Image, ImageDraw, ImageFont, ImageOps
from src.catalog import Catalog

def compute_grid_rows(grid_cols, layout_map, total):
    special_cells = sum(cs * rs for (_, _, cs, rs) in layout_map.values())
    normal_cells = total - len(layout_map)
    total_cells = special_cells + normal_cells
    return -(-total_cells // grid_cols) + 1  # ceil division, +1 for title


def draw_grid(draw, mosaic, font, args, grid_rows, layout_map, images, catalog):
    thumb_size = args.thumb_size
    padding = args.padding
    grid_cols = args.grid_cols

    # Initialize occupancy grid
    occupied = [[False] * grid_cols for _ in range(grid_rows)]

    # Reserve the first row for the title
    for c in range(grid_cols):
        occupied[0][c] = True

    # Draw overall rectangle
    draw.rectangle([padding, padding + thumb_size, padding + grid_cols * thumb_size, padding + grid_rows * thumb_size], outline="gray", width=1)

    def place_object(num, col, row, col_span=1, row_span=1):
        """Place an image or placeholder at the given slot and mark occupied cells."""
        slot_w = col_span * thumb_size
        slot_h = row_span * thumb_size
        x = col * thumb_size + padding
        y = row * thumb_size + padding

        # Draw border first
        draw.rectangle([x, y, x + slot_w, y + slot_h], outline="gray", width=1)

        # Place image or placeholder
        if num in images:
            img = ImageOps.fit(
                images[num],
                (slot_w - 1, slot_h - 1),
                Image.LANCZOS,
                centering=(0.5, 0.5)
            )
            mosaic.paste(img, (x + 1, y + 1))

            # Draw the name on the image (centered at the bottom)
            name_text = catalog.prefix() + f"{num}"
            bbox = draw.textbbox((0, 0), name_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            text_x = x + (slot_w - tw) // 2
            text_y = y + slot_h - th - 20  # 20px padding from bottom
            draw.text((text_x, text_y), name_text, fill="white", font=font)

        else:
            text = catalog.prefix() + f"{num}"
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

    # Place large objects first
    for num, (col, row, col_span, row_span) in layout_map.items():
        place_object(num, col, row+1, col_span, row_span) # Row +1 because title is in 1st row

    # Place remaining small objects
    for i in range(catalog.count()):
        num = i + 1
        if num in layout_map:
            continue  # already placed

        # Find first free 1x1 slot
        placed = False
        for r in range(grid_rows):
            for c in range(grid_cols):
                if not occupied[r][c]:
                    place_object(num, c, r)
                    placed = True
                    break
            if placed:
                break
