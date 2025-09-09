import os
import sys
import subprocess
import re
from PIL import Image, ImageOps

def load_images(input_folder, thumb_size, prefix):
    pattern = re.compile(prefix + r"[-_]?(\d+)")
    images = {}
    for fname in os.listdir(input_folder):
        match = pattern.match(fname)
        if not match:
            continue
        num = int(match.group(1))
        path = os.path.join(input_folder, fname)
        try:
            img = Image.open(path).convert("RGB")
            images[num] = img
        except Exception as e:
            print(f"Error loading {fname}: {e}")

    print(f"Loaded {len(images)} image(s)")
    return images

def open_with_default_viewer(path):
    if sys.platform.startswith("darwin"):      # macOS
        subprocess.run(["open", path])
    elif sys.platform.startswith("win"):       # Windows
        os.startfile(path)
    elif sys.platform.startswith("linux"):     # Linux
        subprocess.run(["xdg-open", path])
