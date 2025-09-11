import os
import sys
import subprocess
import re
from PIL import Image

# Load images from the input folder with a name that starts with 'prefix' and followed by a number
# Returns a dictionary mapping the number to the Image object
def load_images(input_folder: str, prefix: str) -> dict[int, Image.Image]:
    pattern = re.compile(prefix + r"[ _-]?(\d+)")
    images: dict[int, Image.Image] = {}
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

# Open a file with the default image viewer based on the OS
def open_with_default_viewer(path: str):
    if sys.platform.startswith("darwin"):      # macOS
        subprocess.run(["open", path])
    elif sys.platform.startswith("win"):       # Windows
        subprocess.run(["start", "", path], shell=True)
    elif sys.platform.startswith("linux"):     # Linux
        subprocess.run(["xdg-open", path])
