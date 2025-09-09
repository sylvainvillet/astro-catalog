import os
import sys
import subprocess

def open_with_default_viewer(path):
    if sys.platform.startswith("darwin"):      # macOS
        subprocess.run(["open", path])
    elif sys.platform.startswith("win"):       # Windows
        os.startfile(path)
    elif sys.platform.startswith("linux"):     # Linux
        subprocess.run(["xdg-open", path])
