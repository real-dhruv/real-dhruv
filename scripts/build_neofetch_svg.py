"""Build the animated terminal profile card: DHRUV block-letter wordmark + stats."""
import html

OUT = "neofetch.svg"
MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

BG = "#0d1117"
WINDOW = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
GREEN = "#7ee787"
ORANGE = "#ffa657"
BLUE = "#79c0ff"
PINK = "#ff7b72"
DIM = "#8b949e"

BANNER = r"""
██████╗ ██╗  ██╗██████╗ ██╗   ██╗██╗   ██╗
██╔══██╗██║  ██║██╔══██╗██║   ██║██║   ██║
██║  ██║███████║██████╔╝██║   ██║██║   ██║
██║  ██║██╔══██║██╔══██╗██║   ██║╚██╗ ██╔╝
██████╔╝██║  ██║██║  ██║╚██████╔╝ ╚████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═══╝
""".strip("\n").split("\n")

W, H = 1080, 640

def esc(s):
    return html.escape(s, quote=True)

stats = [
    [("Role:      ", ORANGE), ("AI Engineer", BLUE)],
    [("Languages: ", ORANGE), ("TypeScript, Python", BLUE)],
    [("Focus:     ", ORANGE), ("AI agents, automation", BLUE)],
    [("GitHub:    ", ORANGE), ("github.com/real-dhruv", BLUE)],
    [],
    [("GitHub Stats ", PINK), ("-" * 40, DIM)],
    [("Repos: ", ORANGE), ("22", BLUE), (" | ", DIM), ("Followers: ", ORANGE), ("1", BLUE), (" | ", DIM), ("Commits: ", ORANGE), ("228", BLUE)],
]

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'font-family="{MONO}" role="img" aria-label="terminal card for Dhruv Pawar">'
)
parts.append(f'''<defs>
<linearGradient id="wave" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#7ee787"/>
  <stop offset="35%" stop-color="#56d4dd"/>
  <stop offset="70%" stop-color="#79c0ff"/>
  <stop offset="100%" stop-color="#d2a8ff"/>
</linearGradient>
</defs>
<style>
.banner {{ fill: url(#wave); animation: hue 8s linear infinite; }}
@keyframes hue {{ to {{ filter: hue-rotate(360deg); }} }}
.cursor {{ fill: {GREEN}; animation: blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>''')
parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>')
parts.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="12" fill="{WINDOW}" stroke="{BORDER}" stroke-width="1.5"/>')
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{44 + i*26}" cy="46" r="7" fill="{c}"/>')
parts.append(f'<text x="{W//2}" y="52" text-anchor="middle" font-size="15" fill="{DIM}">real-dhruv / README.md</text>')

parts.append(
    f'<text x="52" y="104" font-size="17" xml:space="preserve">'
    f'<tspan fill="{GREEN}">dhruv@github</tspan><tspan fill="{FG}"> ~ % </tspan>'
    f'<tspan fill="{FG}">whoami</tspan></text>'
)
# block-letter banner with animated gradient
parts.append('<text class="banner" font-size="23" xml:space="preserve">')
for i, line in enumerate(BANNER):
    parts.append(f'<tspan x="60" y="{146 + i * 25}">{esc(line)}</tspan>')
parts.append('</text>')
parts.append(
    f'<text x="60" y="322" font-size="17" xml:space="preserve">'
    f'<tspan fill="{DIM}">&gt; </tspan><tspan fill="{FG}">Dhruv Pawar — builds AI agents that ship real work</tspan></text>'
)

parts.append(
    f'<text x="52" y="384" font-size="17" xml:space="preserve">'
    f'<tspan fill="{GREEN}">dhruv@github</tspan><tspan fill="{FG}"> ~ % </tspan>'
    f'<tspan fill="{FG}">neofetch</tspan></text>'
)
y = 420
for row in stats:
    if row:
        spans = "".join(f'<tspan fill="{color}">{esc(txt)}</tspan>' for txt, color in row)
        parts.append(f'<text x="60" y="{y}" font-size="18" xml:space="preserve">{spans}</text>')
    y += 29
parts.append(
    f'<text x="52" y="{y + 8}" font-size="17" xml:space="preserve">'
    f'<tspan fill="{GREEN}">dhruv@github</tspan><tspan fill="{FG}"> ~ % </tspan>'
    f'<tspan class="cursor">█</tspan></text>'
)
parts.append('</svg>')

open(OUT, "w").write("\n".join(parts))
print(f"wrote {OUT}")
