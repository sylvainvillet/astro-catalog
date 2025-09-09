# Astro Catalog

This project generates a mosaic of Messier or Caldwell objects, using images from a local folder.  
The script arranges the objects into a configurable grid, supports larger slots for extended targets (e.g. Andromeda), and overlays labels and a title.  

Perfect for creating a large-format print.

---

## Features

- Loads Messier object images from a folder (`M31.jpg`, `M-31.png`, `M_31.tif`, etc.)
- Places objects on a grid with configurable **columns**, **thumbnail size**, and **layout overrides**
- Supports **multi-cell slots** for large objects (e.g. M31, M42, M45)
- Adds a **title** and **progress counter** if it's not completed yet
- Draws **labels** on images and placeholders for missing ones
- Adjustable **padding** around the mosaic
- Saves as JPEG (default) or PNG

---

## Installation

Requires **Python 3** and **Pillow**:

https://www.python.org/downloads/

```bash
pip install pillow
````

---

## Usage

Prepare a folder with images named like:

* `M31.jpg`
* `M-42.png`
* `M_45.jpeg`

Then run:

```bash
python messier-catalog.py
```

By default, it looks for images in `messier_images/` and saves `messier_mosaic.jpg`.
For the Caldwell catalog, it's the same principle with the `caldwell-catalog.py` script who looks for files starting with "C" in a `caldwell_images/` folder.

---

## Command-line options

All options have defaults but can be overridden:

```bash
python messier-catalog.py --input-folder my_images --output-file mosaic.jpg --grid-cols 20
```

Available arguments:

| Option              | Default                                   | Description                            |
| ------------------- | ----------------------------------------- | -------------------------------------- |
| `--input-folder`    | `messier_images`                          | Folder containing Messier images       |
| `--output-file`     | `messier_mosaic.jpg`                      | Output file path                       |
| `--grid-cols`       | `17`                                      | Number of columns in the grid          |
| `--thumb-size`      | `300`                                     | Thumbnail size (pixels)                |
| `--font-path`       | `/System/Library/Fonts/HelveticaNeue.ttc` | Path to font file                      |
| `--font-size`       | `32`                                      | Font size for labels and placeholders  |
| `--title-font-size` | `124`                                     | Font size for the title                |
| `--padding`         | `20`                                      | Padding around the entire mosaic       |

---

## Example

```bash
python messier-catalog.py --grid-cols 20 --thumb-size 400 --output-file messier_large.png
```

This creates a high-quality PNG 20-column mosaic with larger cells and saves it as `messier_large.png`.