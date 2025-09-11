from PIL import Image, ImageDraw, ImageFont

def draw_title(draw: ImageDraw.ImageDraw, 
               text: str, 
               font: ImageFont.ImageFont | ImageFont.FreeTypeFont, 
               mosaic_w: int, 
               title_row_height: int, 
               padding: int):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (mosaic_w - tw) // 2
    y = padding + (title_row_height - th) // 2
    draw.text((x, y), text, fill="white", font=font)

def draw_progress(draw: ImageDraw.ImageDraw, 
                  text: str, 
                  font: ImageFont.ImageFont | ImageFont.FreeTypeFont, 
                  col: int, 
                  row: int, 
                  padding: int, 
                  thumb_size: int):
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
