from datetime import datetime, timezone
from pathlib import Path

from config import PROFILE, THEMES
from github_api import GitHubStats

FONT = (
    "ui-monospace, Cascadia Code, Cascadia Mono, Segoe UI Mono, "
    "Consolas, Liberation Mono, Menlo, monospace"
)

RANK_RING = {
    "S": 0.95,
    "A+": 0.86,
    "A": 0.77,
    "A-": 0.68,
    "B+": 0.59,
    "B": 0.50,
    "B-": 0.41,
    "C+": 0.32,
    "C": 0.23,
}


def format_number(value: int) -> str:
    return f"{value:,}"


def _count(n: int, singular: str, plural: str | None = None) -> str:
    word = singular if n == 1 else (plural or f"{singular}s")
    return f"{format_number(n)} {word}"


def _n(value: float) -> str:
    rounded = round(value, 2)
    return str(int(rounded)) if rounded == int(rounded) else f"{rounded:.2f}"


def calculate_rank(
    *,
    commits: int,
    pull_requests: int,
    issues: int,
    stars: int,
    repositories: int = 0,
) -> str:
    score = (
        2 * (1 - 2 ** -(commits / 80))
        + 2 * (1 - 2 ** -(pull_requests / 15))
        + 1 * (1 - 2 ** -(issues / 10))
        + 2 * (stars / 15) / (1 + stars / 15)
        + 2 * (repositories / 4) / (1 + repositories / 4)
    ) / 9
    percentile = (1 - score) * 100
    for limit, name in (
        (1, "S"),
        (12.5, "A+"),
        (25, "A"),
        (37.5, "A-"),
        (50, "B+"),
        (62.5, "B"),
        (75, "B-"),
        (87.5, "C+"),
        (100, "C"),
    ):
        if percentile <= limit:
            return name
    return "C"


class SVGCanvas:
    def __init__(self, width: int, height: int, background: str, label: str):
        self.width = width
        self.height = height
        self.background = background
        self.label = label
        self.elements: list[str] = []

    def raw(self, content: str):
        self.elements.append(content)

    def rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        fill: str,
        stroke: str = "none",
        stroke_width: float = 0,
        rx: float = 0,
    ):
        extra = ""
        if stroke != "none":
            extra += f' stroke="{stroke}" stroke-width="{_n(stroke_width)}"'
        if rx:
            extra += f' rx="{_n(rx)}"'
        self.elements.append(
            f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(width)}" '
            f'height="{_n(height)}" fill="{fill}"{extra}/>'
        )

    def text(
        self,
        x: float,
        y: float,
        content: str,
        size: int = 18,
        fill: str = "#FFFFFF",
        weight: str = "normal",
        extra: str = "",
        letter_spacing: str | None = None,
    ):
        spacing = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
        extra_attr = f" {extra}" if extra else ""
        escaped = (
            content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        self.elements.append(
            f'<text x="{_n(x)}" y="{_n(y)}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{spacing}{extra_attr}>{escaped}</text>'
        )

    def language_bar(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        segments: list[tuple[str, float]],
        track: str,
    ):
        total = sum(max(frac, 0.0) for _, frac in segments)
        if total <= 0:
            self.rect(x, y, width, height, fill=track, rx=height / 2)
            return
        clip_id = "langbar"
        radius = height / 2
        self.raw(
            f'<defs><clipPath id="{clip_id}">'
            f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(width)}" '
            f'height="{_n(height)}" rx="{_n(radius)}"/></clipPath></defs>'
        )
        self.rect(x, y, width, height, fill=track, rx=radius)
        self.raw(f'<g clip-path="url(#{clip_id})">')
        offset = 0.0
        for i, (color, fraction) in enumerate(segments):
            if fraction <= 0:
                continue
            seg_w = width * (fraction / total)
            if i == len(segments) - 1:
                seg_w = width - offset
            begin = f"{0.35 + i * 0.08:.2f}s"
            self.raw(
                f'<rect x="{_n(x + offset)}" y="{_n(y)}" width="{_n(seg_w)}" '
                f'height="{_n(height)}" fill="{color}">'
                f'<animate attributeName="width" from="0" to="{_n(seg_w)}" '
                f'dur="0.7s" begin="{begin}" fill="freeze"/></rect>'
            )
            offset += seg_w
        self.raw("</g>")

    def save(self, filename: str):
        body = "\n".join(self.elements)
        Path(filename).write_text(
            f"""<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-label="{self.label}">
<rect width="100%" height="100%" fill="{self.background}"/>
{body}
</svg>
""",
            encoding="utf-8",
        )


class _Card:
    def __init__(self, theme: str, width: int, height: int, label: str):
        self.colors = THEMES[theme]
        self.canvas = SVGCanvas(width, height, self.colors["background"], label)


class BannerRenderer(_Card):
    def __init__(self, theme: str):
        super().__init__(theme, 900, 300, f"{PROFILE.name} profile banner")

    def render(self, stats: GitHubStats, output_file: str):
        c, col = self.canvas, self.colors
        year = datetime.now(timezone.utc).year
        name = PROFILE.name.upper()
        c.rect(16, 16, 868, 268, fill=col["surface"], stroke=col["border"], stroke_width=1, rx=8)
        underline_to = min(860, 40 + int(len(name) * 20))
        c.raw(
            f'<line x1="40" y1="78" x2="{underline_to}" y2="78" '
            f'stroke="{col["accent"]}" stroke-width="2">'
            f'<animate attributeName="x2" from="40" to="{underline_to}" '
            f'dur="0.8s" begin="0.15s" fill="freeze"/></line>'
        )
        c.text(40, 64, name, size=32, fill=col["title"], weight="700", letter_spacing="1.5")
        c.text(40, 106, PROFILE.tagline, size=14, fill=col["text"])
        c.text(40, 130, PROFILE.stack_line, size=13, fill=col["secondary"])
        c.text(
            40,
            164,
            f"{_count(stats.repositories, 'repo')}   ·   "
            f"{_count(stats.stars, 'star')}   ·   "
            f"{_count(stats.followers, 'follower')}",
            size=14,
            fill=col["accent"],
            weight="600",
        )
        c.text(
            40,
            188,
            f"{year}  ·  {_count(stats.commits, 'commit')}   ·   "
            f"{_count(stats.pull_requests, 'PR')}   ·   "
            f"{_count(stats.issues, 'issue')}",
            size=13,
            fill=col["text"],
        )
        c.text(40, 220, "languages", size=12, fill=col["secondary"])
        langs = stats.languages[:5]
        if langs:
            c.language_bar(
                40,
                232,
                820,
                8,
                [(lang.color, lang.percentage) for lang in langs],
                col["bar_track"],
            )
            slot = 820 / len(langs)
            for i, lang in enumerate(langs):
                x = 40 + i * slot
                c.rect(x, 252, 8, 8, fill=lang.color, rx=2)
                c.text(
                    x + 14,
                    260,
                    f"{lang.name} {lang.percentage:g}%",
                    size=11,
                    fill=col["text"],
                )
        else:
            c.text(40, 248, "—", size=14, fill=col["secondary"])
        c.save(output_file)


class StreakRenderer(_Card):
    def __init__(self, theme: str):
        super().__init__(theme, 495, 195, f"{PROFILE.name} GitHub streak")

    def render(self, stats: GitHubStats, output_file: str):
        c, col = self.canvas, self.colors
        year = datetime.now(timezone.utc).year
        c.rect(8, 8, 479, 179, fill=col["surface"], stroke=col["border"], stroke_width=1, rx=12)
        columns = (
            (90, "Contributions", format_number(stats.contributions), col["title"], str(year), 26),
            (
                247,
                "Current streak",
                str(stats.current_streak),
                col["accent"],
                stats.current_streak_range or "—",
                34,
            ),
            (
                404,
                "Longest streak",
                str(stats.longest_streak),
                col["title"],
                stats.longest_streak_range or "—",
                26,
            ),
        )
        mid = 'text-anchor="middle"'
        for x, title, value, color, subtitle, size in columns:
            c.text(x, 52, title, size=11, fill=col["secondary"], extra=mid)
            c.text(x, 102, value, size=size, fill=color, weight="700", extra=mid)
            c.text(x, 132, subtitle, size=11, fill=col["secondary"], extra=mid)
        c.save(output_file)


class StatsRenderer(_Card):
    def __init__(self, theme: str):
        super().__init__(theme, 495, 195, f"{PROFILE.name} GitHub stats")

    def render(self, stats: GitHubStats, output_file: str):
        c, col = self.canvas, self.colors
        year = datetime.now(timezone.utc).year
        letter = calculate_rank(
            commits=stats.commits,
            pull_requests=stats.pull_requests,
            issues=stats.issues,
            stars=stats.stars,
            repositories=stats.repositories,
        )
        c.rect(8, 8, 479, 179, fill=col["surface"], stroke=col["border"], stroke_width=1, rx=12)
        c.text(28, 40, "GitHub Stats", size=14, fill=col["accent"], weight="700")
        y = 70
        for label, value in (
            ("Stars", format_number(stats.stars)),
            (f"Commits ({year})", format_number(stats.commits)),
            ("PRs", format_number(stats.pull_requests)),
            ("Issues", format_number(stats.issues)),
            ("Repos", format_number(stats.repositories)),
        ):
            c.text(28, y, label, size=12, fill=col["secondary"])
            c.text(188, y, value, size=13, fill=col["title"], weight="700")
            y += 22

        cx, cy, radius = 355, 98, 50
        circ = 2 * 3.1415926535 * radius
        visible = circ * RANK_RING[letter]
        c.raw(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{col["surface"]}" '
            f'stroke="{col["bar_track"]}" stroke-width="10"/>'
        )
        c.raw(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{col["accent"]}" stroke-width="10" stroke-linecap="round" '
            f'transform="rotate(-90 {cx} {cy})" stroke-dasharray="{circ:.2f}" '
            f'stroke-dashoffset="{circ - visible:.2f}">'
            f'<animate attributeName="stroke-dashoffset" from="{circ:.2f}" '
            f'to="{circ - visible:.2f}" dur="1.1s" fill="freeze"/></circle>'
        )
        c.text(
            cx,
            cy,
            letter,
            size=28 if len(letter) > 1 else 34,
            fill=col["title"],
            weight="700",
            extra='text-anchor="middle" dominant-baseline="middle"',
        )
        c.text(cx, 168, "Rank", size=11, fill=col["secondary"], extra='text-anchor="middle"')
        c.save(output_file)
