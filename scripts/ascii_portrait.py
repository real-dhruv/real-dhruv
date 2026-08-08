"""Convert a portrait photo into neofetch-style ASCII art.

Approach modeled on classic neofetch face art: only clearly dark features
(hair, glasses, brows, eyes, mustache) get dense characters; skin midtones
map to sparse dots or whitespace so the face stays readable, and the
background is masked out entirely.
"""
import sys
from PIL import Image, ImageOps, ImageFilter

SRC = sys.argv[1]
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 50
ROWS = int(sys.argv[3]) if len(sys.argv) > 3 else 40

img = Image.open(SRC).convert("L")
w, h = img.size
# tight head crop: hair to chin/neck, small shoulder hint
img = img.crop((int(w * 0.22), int(h * 0.12), int(w * 0.78), int(h * 0.92)))
img = ImageOps.autocontrast(img, cutoff=1)
img = img.filter(ImageFilter.SMOOTH)
img = img.resize((COLS, ROWS))
px = img.load()

# head-shaped mask: ellipse for the skull + wider ellipse low for shoulders
cx = COLS / 2.0

def inside(x, y):
    fy = y / ROWS
    head = ((x - cx) / (COLS * 0.34)) ** 2 + ((y - ROWS * 0.38) / (ROWS * 0.40)) ** 2 <= 1.0
    torso = fy > 0.72 and ((x - cx) / (COLS * 0.46)) ** 2 + ((y - ROWS * 1.05) / (ROWS * 0.38)) ** 2 <= 1.0
    return head or torso

# levels: dark features get ink, midtones (skin) go sparse, light -> space
def char_for(v):
    if v < 55:
        return "@"
    if v < 80:
        return "#"
    if v < 100:
        return "%"
    if v < 118:
        return "x"
    if v < 135:
        return "/"
    if v < 152:
        return ";"
    if v < 170:
        return ","
    if v < 188:
        return "."
    return " "

lines = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        v = px[x, y]
        if y / ROWS > 0.74:  # lighten the shirt so it doesn't read as a solid block
            v = min(255, v + 55)
        row.append(char_for(v) if inside(x, y) else " ")
    lines.append("".join(row).rstrip())

print("\n".join(lines))
