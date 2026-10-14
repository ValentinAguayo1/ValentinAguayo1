"""Generate assets/card.svg: a neofetch-style profile card with an ASCII portrait.

Usage: python3 scripts/make_card.py   (needs: pip install pillow)
Edit PROFILE / PROJECTS below; GitHub numbers are fetched live.
assets/photo.png must have a transparent background (it was cut out once with `rembg`).
"""

import json
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
USER = "ValentinAguayo1"
PHOTO = ROOT / "assets/photo.png"
OUT = ROOT / "assets/card.svg"

PROFILE = [
    ("OS", "Linux"),
    ("Location", "Chile"),
    ("Role", "Software Engineer"),
    ("Focus", "Backend & Automation"),
    ("Status", "Open to work"),
    ("IDE", "VS Code, Cursor"),
    None,
    ("Languages.Programming", "Python, TypeScript, SQL"),
    ("Languages.Real", "Spanish, English"),
    ("Frameworks", "Angular, Firebase"),
    ("Quality", "Pytest, Ruff, GitHub Actions"),
    ("AI", "ChatGPT, Gemini, Claude"),
]
PROJECTS = [
    ("GH Summary CLI", "Python CLI for GitHub profiles"),
    ("TaskFlow", "Angular + Firebase task manager"),
    ("Shop Admin", "TypeScript dashboard (WIP)"),
]

COLS = 52                    # ASCII grid width; rows follow the photo's aspect ratio
CROP = (190, 10, 670, 640)   # photo box around the head/shoulders (left, top, right, bottom)
RAMP = " .:-=+*#%@"          # dark -> bright, like a lit face on a dark terminal

FONT = 12
CW, LH = FONT * 0.6, FONT * 1.25   # monospace cell size
PANEL_COLS = 58
PAD = 36

C = dict(bg="#0d1117", border="#30363d", key="#f0883e", val="#e6edf3",
         dot="#484f58", hdr="#58a6ff", ascii="#c9d1d9", bar="#3fb950", muted="#8b949e")


def ascii_portrait() -> list[str]:
    im = Image.open(PHOTO).convert("RGBA").crop(CROP)
    w, h = im.size
    rows = round(COLS * h / w * CW / LH)
    luma = ImageOps.grayscale(im).resize((COLS, rows), Image.BOX).load()
    alpha = im.getchannel("A").resize((COLS, rows), Image.BOX).load()
    lines = []
    for y in range(rows):
        line = ""
        for x in range(COLS):
            if alpha[x, y] < 128:
                line += " "
            else:  # subject pixels never go blank, so hair and shirt keep a silhouette
                line += RAMP[1 + min(len(RAMP) - 2, int(luma[x, y] / 160 * (len(RAMP) - 1)))]
        lines.append(line.rstrip())
    return lines


def gh(url: str):
    token = os.environ.get("GITHUB_TOKEN")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"} if token else {})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def github_stats():
    user = gh(f"https://api.github.com/users/{USER}")
    repos = gh(f"https://api.github.com/users/{USER}/repos?per_page=100")
    stars = sum(r["stargazers_count"] for r in repos)
    langs: dict[str, int] = {}
    for r in repos:
        for name, n in gh(r["languages_url"]).items():
            langs[name] = langs.get(name, 0) + n
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    return user["public_repos"], user["followers"], stars, [(k, v / total) for k, v in top]


def kv(key: str, val: str, width=PANEL_COLS) -> str:
    dots = "." * max(1, width - len(key) - len(val) - 3)
    return (f'<tspan fill="{C["key"]}">{escape(key)}:</tspan> '
            f'<tspan fill="{C["dot"]}">{dots}</tspan> '
            f'<tspan fill="{C["val"]}">{escape(val)}</tspan>')


def header(title: str, width=PANEL_COLS) -> str:
    rule = "─" * (width - len(title) - 3)
    return f'<tspan fill="{C["hdr"]}">─ {escape(title)} </tspan><tspan fill="{C["dot"]}">{rule}</tspan>'


def main():
    repos, followers, stars, top = github_stats()
    portrait = ascii_portrait()

    panel: list[str | None] = [f'<tspan fill="{C["hdr"]}" font-weight="bold">{USER}@github</tspan>'
                               f'<tspan fill="{C["dot"]}"> {"─" * (PANEL_COLS - len(USER) - 8)}</tspan>', None]
    panel += [kv(*p) if p else None for p in PROFILE]
    panel += [None, header("Projects")] + [kv(*p) for p in PROJECTS]
    stats = [kv("Repos", str(repos)), kv("Followers", str(followers))]
    if stars:
        stats.insert(1, kv("Stars", str(stars)))
    panel += [None, header("GitHub Stats"), *stats, None, header("Languages")]
    top_share = top[0][1] if top else 1
    for name, share in top:
        bar = "█" * max(1, round(share / top_share * 24))
        panel.append(f'<tspan fill="{C["key"]}">{escape(name.lower()):<12}</tspan>'
                     f'<tspan fill="{C["bar"]}">{bar:<24}</tspan>'
                     f'<tspan fill="{C["muted"]}"> {share * 100:5.1f}%</tspan>')

    left_w = COLS * CW
    right_x = PAD + left_w + PAD
    width = right_x + PANEL_COLS * CW + PAD
    height = PAD + max(len(portrait), len(panel)) * LH + PAD

    def text(x, y, inner, fill=None):
        f = f' fill="{fill}"' if fill else ""
        return f'<text x="{x:.1f}" y="{y:.1f}" xml:space="preserve"{f}>{inner}</text>'

    body = [text(PAD, PAD + (i + 1) * LH, escape(line), C["ascii"]) for i, line in enumerate(portrait) if line]
    body += [text(right_x, PAD + (i + 1) * LH, line) for i, line in enumerate(panel) if line]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">
<rect width="100%" height="100%" rx="14" fill="{C["bg"]}" stroke="{C["border"]}"/>
<g font-family="'Fira Code','Cascadia Code','JetBrains Mono',Consolas,'DejaVu Sans Mono',monospace" font-size="{FONT}">
{chr(10).join(body)}
</g>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({width:.0f}x{height:.0f})")


if __name__ == "__main__":
    main()
