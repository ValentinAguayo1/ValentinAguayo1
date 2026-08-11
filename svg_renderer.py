from config import PROFILE, THEMES
from models import GitHubStats
from svg_canvas import SVGCanvas
from utils import current_timestamp, format_number


class SVGRenderer:
    WIDTH = 900
    HEIGHT = 320

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

        c.rect(
            x=16,
            y=16,
            width=868,
            height=288,
            fill=col["surface"],
            stroke=col["border"],
            stroke_width=1,
            rx=4,
        )

        # Accent underline (x2 final for no-SMIL clients; animates when supported)
        c.raw(
            f'<line x1="40" y1="86" x2="280" y2="86" '
            f'stroke="{col["accent"]}" stroke-width="2">'
            f'<animate attributeName="x2" from="40" to="280" '
            f'dur="0.8s" begin="0.15s" fill="freeze"/>'
            f"</line>"
        )

        c.text(
            40,
            72,
            PROFILE.name.upper(),
            size=34,
            fill=col["title"],
            weight="700",
            letter_spacing="1.5",
        )

        c.text(40, 118, PROFILE.tagline, size=15, fill=col["text"])
        c.text(40, 148, PROFILE.stack_line, size=13, fill=col["secondary"])

        metrics = (
            f"{format_number(stats.repositories)} repos"
            f"   ·   {format_number(stats.stars)} stars"
            f"   ·   {format_number(stats.followers)} followers"
        )
        c.text(40, 190, metrics, size=14, fill=col["accent"], weight="600")

        c.text(40, 224, "languages", size=12, fill=col["secondary"])

        if stats.languages:
            segments = [
                (lang.color, lang.percentage / 100.0) for lang in stats.languages
            ]
            c.language_bar(
                x=40,
                y=236,
                width=820,
                height=8,
                segments=segments,
                track=col["bar_track"],
            )

            label_x = 40.0
            for lang in stats.languages[:4]:
                label = f"{lang.name} {lang.percentage:g}%"
                c.text(round(label_x, 1), 268, label, size=12, fill=col["text"])
                # ponytail: monospace width approx; fine for ≤4 labels
                label_x += len(label) * 7.4 + 28
        else:
            c.text(40, 252, "—", size=14, fill=col["secondary"])

        c.line(40, 286, 860, 286, col["border"])
        c.text(
            40,
            306,
            f"auto-generated · updated {current_timestamp()}",
            size=11,
            fill=col["secondary"],
        )

        c.save(output_file)
