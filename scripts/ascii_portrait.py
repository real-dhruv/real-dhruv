"""Convert a portrait photo into neofetch-style ASCII art.

Readability strategy: ink ONLY where the image has dark masses (hair,
glasses, eyes, mustache, shirt) or strong edges (face outline, features).
Flat midtones — skin, background — stay whitespace, which is what makes
classic README ASCII portraits legible.
"""
import sys
from PIL import Image, ImageOps, ImageFilter

SRC = sys.argv[1]
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 58
ROWS = int(sys.argv[3]) if len(sys.argv) > 3 else 46

img = Image.open(SRC).convert("L")
w, h = img.size
img = img.crop((int(w * 0.20), int(h * 0.10), int(w * 0.80), int(h * 0.95)))
img = ImageOps.autocontrast(img, cutoff=1)

tone = img.filter(ImageFilter.GaussianBlur(2)).resize((COLS, ROWS))
edges = img.filter(ImageFilter.GaussianBlur(1)).filter(ImageFilter.FIND_EDGES)
edges = edges.filter(ImageFilter.MaxFilter(5)).resize((COLS, ROWS))

tp, ep = tone.load(), edges.load()
cx = COLS / 2.0

def inside(x, y):
    fy = y / ROWS
    head = ((x - cx) / (COLS * 0.36)) ** 2 + ((y - ROWS * 0.36) / (ROWS * 0.40)) ** 2 <= 1.0
    torso = fy > 0.70 and ((x - cx) / (COLS * 0.48)) ** 2 + ((y - ROWS * 1.08) / (ROWS * 0.42)) ** 2 <= 1.0
    return head or torso

# dark-mass glyphs (by darkness) and edge glyphs (by edge strength)
def dark_char(v):
    if v < 45:
        return "@"
    if v < 70:
        return "&"
    if v < 90:
        return "8"
    return "m"

def edge_char(e):
    if e > 200:
        return "%"
    if e > 150:
        return "j"
    return "/"

lines = []
for y in range(ROWS):
    fy = y / ROWS
    row = []
    for x in range(COLS):
        if not inside(x, y):
            row.append(" ")
            continue
        v, e = tp[x, y], ep[x, y]
        if fy > 0.74:
            v += 65  # shirt: keep as light texture, not a slab
        if v < 105:
            row.append(dark_char(v))
        elif e > 110 and v < 190:
            row.append(edge_char(e))
        elif v < 125:
            row.append(";")
        else:
            row.append(" ")
    lines.append("".join(row).rstrip())

print("\n".join(lines))
