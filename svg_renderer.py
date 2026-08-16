from datetime import datetime, timezone

from config import PROFILE, THEMES
from models import GitHubStats
from svg_canvas import SVGCanvas
from utils import calculate_rank, current_timestamp, format_number


class SVGRenderer:
    WIDTH = 900
    HEIGHT = 340

    def __init__(self, theme: str):
        if theme not in THEMES:
            raise ValueError(f"Invalid theme '{theme}'.")

        self.colors = THEMES[theme]
        self.canvas = SVGCanvas(
            width=self.WIDTH,
            height=self.HEIGHT,
            background=self.colors["background"],
        )

    def render(self, stats: GitHubStats, output_file: str):
        c = self.canvas
        col = self.colors
        year = datetime.now(timezone.utc).year

        c.rect(
            x=16,
            y=16,
            width=868,
            height=308,
            fill=col["surface"],
            stroke=col["border"],
            stroke_width=1,
            rx=4,
        )

        # Accent underline (x2 final for no-SMIL clients; animates when supported)
        c.raw(
            f'<line x1="40" y1="82" x2="280" y2="82" '
            f'stroke="{col["accent"]}" stroke-width="2">'
            f'<animate attributeName="x2" from="40" to="280" '
            f'dur="0.8s" begin="0.15s" fill="freeze"/>'
            f"</line>"
        )

        c.text(
            40,
            68,
            PROFILE.name.upper(),
            size=32,
            fill=col["title"],
            weight="700",
            letter_spacing="1.5",
        )

        c.text(40, 112, PROFILE.tagline, size=14, fill=col["text"])
        c.text(40, 140, PROFILE.stack_line, size=13, fill=col["secondary"])

        metrics = (
            f"{format_number(stats.repositories)} repos"
            f"   ·   {format_number(stats.stars)} stars"
            f"   ·   {format_number(stats.followers)} followers"
        )
        c.text(40, 176, metrics, size=14, fill=col["accent"], weight="600")

        year_metrics = (
            f"{year}  ·  {format_number(stats.commits)} commits"
            f"   ·   {format_number(stats.pull_requests)} PRs"
            f"   ·   {format_number(stats.issues)} issues"
        )
        c.text(40, 200, year_metrics, size=13, fill=col["text"])

        c.text(40, 232, "languages", size=12, fill=col["secondary"])

        if stats.languages:
            segments = [
                (lang.color, lang.percentage / 100.0) for lang in stats.languages
            ]
            c.language_bar(
                x=40,
                y=244,
                width=820,
                height=8,
                segments=segments,
                track=col["bar_track"],
            )

            label_x = 40.0
            for lang in stats.languages[:4]:
                label = f"{lang.name} {lang.percentage:g}%"
                c.text(round(label_x, 1), 276, label, size=12, fill=col["text"])
                # ponytail: monospace width approx; fine for ≤4 labels
                label_x += len(label) * 7.4 + 28
        else:
            c.text(40, 260, "—", size=14, fill=col["secondary"])

        c.line(40, 300, 860, 300, col["border"])
        c.text(
            40,
            322,
            f"auto-generated · updated {current_timestamp()}",
            size=11,
            fill=col["secondary"],
        )

        c.save(output_file)


class StreakRenderer:
    WIDTH = 495
    HEIGHT = 195

    def __init__(self, theme: str):
        if theme not in THEMES:
            raise ValueError(f"Invalid theme '{theme}'.")
        self.colors = THEMES[theme]
        self.canvas = SVGCanvas(
            width=self.WIDTH,
            height=self.HEIGHT,
            background=self.colors["background"],
        )

    def render(self, stats: GitHubStats, output_file: str):
        c = self.canvas
        col = self.colors
        created = datetime.fromisoformat(
            stats.created_at.replace("Z", "+00:00")
        ).year if stats.created_at else 2022

        c.rect(
            x=8,
            y=8,
            width=479,
            height=179,
            fill=col["surface"],
            stroke=col["border"],
            stroke_width=1,
            rx=12,
        )

        columns = [
            (90, "Total Contributions", format_number(stats.contributions), col["title"], f"{created} - Present", 26),
            (247, "Current Streak", str(stats.current_streak), col["accent"], stats.current_streak_range or "—", 34),
            (404, "Longest Streak", str(stats.longest_streak), col["title"], stats.longest_streak_range or "—", 26),
        ]
        for x, title, value, color, subtitle, size in columns:
            c.text(x, 52, title, size=11, fill=col["secondary"], extra='text-anchor="middle"')
            c.text(x, 102, value, size=size, fill=color, weight="700", extra='text-anchor="middle"')
            c.text(x, 132, subtitle, size=11, fill=col["secondary"], extra='text-anchor="middle"')

        c.save(output_file)


class StatsRenderer:
    WIDTH = 495
    HEIGHT = 195

    def __init__(self, theme: str):
        if theme not in THEMES:
            raise ValueError(f"Invalid theme '{theme}'.")
        self.colors = THEMES[theme]
        self.canvas = SVGCanvas(
            width=self.WIDTH,
            height=self.HEIGHT,
            background=self.colors["background"],
        )

    def render(self, stats: GitHubStats, output_file: str):
        c = self.canvas
        col = self.colors
        letter, percentile = calculate_rank(
            commits=stats.commits,
            pull_requests=stats.pull_requests,
            issues=stats.issues,
            stars=stats.stars,
            followers=stats.followers,
        )

        c.rect(
            x=8,
            y=8,
            width=479,
            height=179,
            fill=col["surface"],
            stroke=col["border"],
            stroke_width=1,
            rx=12,
        )

        c.text(28, 40, "GitHub Stats", size=14, fill=col["accent"], weight="700")

        rows = [
            ("Total Stars", format_number(stats.stars)),
            ("Total Commits", format_number(stats.commits)),
            ("Total PRs", format_number(stats.pull_requests)),
            ("Total Issues", format_number(stats.issues)),
            ("Repos", format_number(stats.repositories)),
        ]
        y = 70
        for label, value in rows:
            c.text(28, y, label, size=12, fill=col["secondary"])
            c.text(188, y, value, size=13, fill=col["title"], weight="700")
            y += 22

        # Center of the right pane (stats end ~220, card inner right 487)
        cx, cy, radius = 355, 98, 50
        circ = 2 * 3.1415926535 * radius
        fill_ratio = max(0.12, 1 - percentile / 100)
        visible = circ * fill_ratio
        c.raw(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{col["background"]}" '
            f'stroke="{col["bar_track"]}" stroke-width="10"/>'
        )
        c.raw(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{col["accent"]}" stroke-width="10" '
            f'stroke-linecap="round" transform="rotate(-90 {cx} {cy})" '
            f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ - visible:.2f}">'
            f'<animate attributeName="stroke-dashoffset" from="{circ:.2f}" '
            f'to="{circ - visible:.2f}" dur="1.1s" fill="freeze"/>'
            f"</circle>"
        )
        c.text(
            cx,
            cy + 12,
            letter,
            size=36,
            fill=col["title"],
            weight="700",
            extra='text-anchor="middle"',
        )
        c.text(
            cx,
            168,
            "Rank",
            size=11,
            fill=col["secondary"],
            extra='text-anchor="middle"',
        )

        c.save(output_file)
