from special_objects import SpecialObject
from parameters import Parameters
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Compute the number of grid rows needed based on columns, layout map, and total items
def compute_grid_rows(grid_cols: int, 
                      special_objects: list[SpecialObject], 
                      total: int) -> int:
    special_cells = sum(obj.cells() for obj in special_objects)
    normal_cells = total - sum(obj.objects() for obj in special_objects)
    total_cells = special_cells + normal_cells
    return -(-total_cells // grid_cols) + 1  # ceil division, +1 for title

# Draw the grid and place images according to the layout map
def draw_grid(draw: ImageDraw.ImageDraw, 
              mosaic: Image.Image, 
              font: ImageFont.ImageFont | ImageFont.FreeTypeFont, 
              params: Parameters, 
              grid_rows: int, 
              special_objects: list[SpecialObject], 
              images: dict[int, Image.Image]):
    thumb_size = params.get_thumb_size_scaled()
    padding = params.get_padding_scaled()
    grid_cols = params.grid_cols

    # Initialize occupancy grid
    occupied = [[False] * grid_cols for _ in range(grid_rows)]

    # Reserve the first row for the title
    for c in range(grid_cols):
        occupied[0][c] = True

    # Draw overall rectangle
    draw.rectangle([padding, padding + thumb_size, padding + grid_cols * thumb_size, padding + grid_rows * thumb_size], outline="gray", width=1)

    def place_object(numbers: list[int], col: int, row: int, col_span: int = 1, row_span: int = 1):
        """Place an image or placeholder at the given slot and mark occupied cells."""
        slot_w = col_span * thumb_size
        slot_h = row_span * thumb_size
        x = col * thumb_size + padding
        y = row * thumb_size + padding
        name_text = ", ".join(params.catalog.prefix() + f"{num}" for num in numbers)

        # Place image or placeholder
        if any(num in images for num in numbers):
            image = next(img for num, img in images.items() if num in numbers)
            img = ImageOps.fit(
                image,
                (slot_w, slot_h),
                Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )
            mosaic.paste(img, (x + 1, y + 1))

            # Draw the name on the image (centered at the bottom), list the names if multiple
            bbox = draw.textbbox((0, 0), name_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            text_x = x + (slot_w - tw) // 2
            text_y = y + slot_h - th - params.get_label_bottom_space_scaled()
            draw.text((text_x, text_y), name_text, fill="white", font=font)

        else:
            bbox = draw.textbbox((0, 0), name_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(
                (x + (slot_w - tw) // 2, y + (slot_h - th) // 2),
                name_text,
                fill="white",
                font=font
            )

        # Draw border
        draw.rectangle([x, y, x + slot_w, y + slot_h], outline="gray", width=1)

        # Mark cells as occupied
        for r in range(row, row + row_span):
            for c in range(col, col + col_span):
                if r < grid_rows and c < grid_cols:
                    occupied[r][c] = True

    # Place large objects first
    for special in special_objects:
        place_object(special.numbers, special.x - 1, special.y, special.width, special.height)

    # Place remaining small objects
    for i in range(params.catalog.count()):
        num = i + 1
        if any(num in special.numbers for special in special_objects):
            continue  # already placed

        # Find first free 1x1 slot
        placed = False
        for r in range(grid_rows):
            for c in range(grid_cols):
                if not occupied[r][c]:
                    place_object([num], c, r)
                    placed = True
                    break
            if placed:
                break
