"""Convert a portrait photo into neofetch-style ASCII art.

The photo has a bright, busy landscape background; an elliptical vignette
mask fades everything outside the face/torso region to white so only the
subject renders as characters.
"""
import sys
from PIL import Image, ImageEnhance, ImageOps

SRC = sys.argv[1]
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 46
ROWS = int(sys.argv[3]) if len(sys.argv) > 3 else 42
# dark -> light
RAMP = "@%#WM8B&$Xhkbdpqwmzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

img = Image.open(SRC).convert("L")
img = ImageOps.autocontrast(img, cutoff=2)
img = ImageEnhance.Contrast(img).enhance(1.35)

w, h = img.size
# crop a touch tighter around the subject (center-weighted)
img = img.crop((int(w * 0.08), int(h * 0.02), int(w * 0.92), h))
w, h = img.size

img = img.resize((COLS, ROWS))
px = img.load()

# elliptical mask centred slightly below middle (face + shoulders)
cx, cy = COLS / 2.0, ROWS * 0.50
rx, ry = COLS * 0.50, ROWS * 0.56

lines = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
        v = px[x, y]
        if d > 1.0 or v >= 232:  # outside mask, or bright sky/highlight
            row.append(" ")
            continue
        if d > 0.80:  # soft edge: lighten toward the rim
            v = min(255, int(v + (d - 0.80) / 0.20 * 150))
        row.append(RAMP[min(len(RAMP) - 1, v * len(RAMP) // 256)])
    lines.append("".join(row).rstrip())

print("\n".join(lines))
