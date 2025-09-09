def draw_title(draw, text, font, mosaic_w, title_row_height, padding):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (mosaic_w - tw) // 2
    y = padding + (title_row_height - th) // 2
    draw.text((x, y), text, fill="white", font=font)

def draw_progress(draw, text, font, col, row, padding, thumb_size):
    x = col * thumb_size + padding
    y = row * thumb_size + padding
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        (x + (thumb_size * 2 - tw) // 2, y + (thumb_size - th) // 2),
        text,
        fill="white",
        font=font
    )
