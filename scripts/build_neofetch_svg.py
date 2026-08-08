"""Build the neofetch-style profile card SVG from ascii.txt."""
import html

ASCII_PATH = "ascii.txt"
OUT = "neofetch.svg"

MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

# GitHub-dark-inspired terminal palette
BG = "#0d1117"
WINDOW = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
GREEN = "#7ee787"
ORANGE = "#ffa657"
BLUE = "#79c0ff"
PINK = "#ff7b72"
DIM = "#8b949e"

art_lines = open(ASCII_PATH).read().rstrip("\n").split("\n")

W, H = 1080, 700
ART_X, ART_Y, ART_FS, ART_LH = 52, 128, 12.5, 14
ST_X, ST_Y, ST_FS, ST_LH = 470, 190, 19, 34

def esc(s):
    return html.escape(s, quote=True)

stats = [
    [("User:      ", ORANGE), ("Dhruv Pawar", BLUE)],
    [("Languages: ", ORANGE), ("TypeScript, Python", BLUE)],
    [("Focus:     ", ORANGE), ("AI agents, automation", BLUE)],
    [("GitHub:    ", ORANGE), ("github.com/real-dhruv", BLUE)],
    [],
    [("GitHub Stats ", PINK), ("-" * 28, DIM)],
    [("Repos: ", ORANGE), ("22", BLUE), (" | ", DIM), ("Followers: ", ORANGE), ("1", BLUE), (" | ", DIM), ("Commits: ", ORANGE), ("228", BLUE)],
]

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'font-family="{MONO}" role="img" aria-label="neofetch card for Dhruv Pawar">'
)
parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
parts.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="12" fill="{WINDOW}" stroke="{BORDER}" stroke-width="1.5"/>')
# window dots
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{44 + i*26}" cy="46" r="7" fill="{c}"/>')
parts.append(f'<text x="{W//2}" y="52" text-anchor="middle" font-size="15" fill="{DIM}">real-dhruv / README.md</text>')
# prompt line
parts.append(
    f'<text x="52" y="94" font-size="17" xml:space="preserve">'
    f'<tspan fill="{GREEN}">dhruv@github</tspan><tspan fill="{FG}"> ~ % </tspan>'
    f'<tspan fill="{GREEN}">neofetch</tspan></text>'
)
# ascii art
parts.append(f'<text font-size="{ART_FS}" fill="{FG}" xml:space="preserve">')
for i, line in enumerate(art_lines):
    parts.append(f'<tspan x="{ART_X}" y="{ART_Y + i*ART_LH:.1f}">{esc(line)}</tspan>')
parts.append('</text>')
# stats column
y = ST_Y
for row in stats:
    if row:
        spans = "".join(f'<tspan fill="{color}">{esc(txt)}</tspan>' for txt, color in row)
        parts.append(f'<text x="{ST_X}" y="{y}" font-size="{ST_FS}" xml:space="preserve">{spans}</text>')
    y += ST_LH
parts.append('</svg>')

open(OUT, "w").write("\n".join(parts))
print(f"wrote {OUT}, {len(art_lines)} art lines")
