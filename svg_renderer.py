from config import PROFILE, THEMES
from models import GitHubStats
from svg_canvas import SVGCanvas
from utils import current_timestamp


class SVGRenderer:
    WIDTH = 900
    HEIGHT = 380

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

        # Main card
        c.rect(
            x=20,
            y=20,
            width=860,
            height=340,
            fill=self.colors["card"],
            stroke=self.colors["border"],
            stroke_width=1,
            rx=16,
        )

        # Profile
        c.text(
            45,
            60,
            PROFILE.name,
            size=30,
            fill=self.colors["title"],
            weight="bold",
        )

        c.text(
            45,
            90,
            PROFILE.role,
            size=17,
            fill=self.colors["secondary"],
        )

        c.text(
            45,
            115,
            PROFILE.location,
            size=14,
            fill=self.colors["secondary"],
        )

        c.text(
            45,
            140,
            PROFILE.bio,
            size=14,
            fill=self.colors["text"],
        )

        c.line(
            45,
            165,
            855,
            165,
            self.colors["border"],
        )

        # Statistics title
        c.text(
            45,
            195,
            "GitHub Statistics",
            size=18,
            fill=self.colors["title"],
            weight="bold",
        )

        card_width = 100
        card_height = 90
        gap = 10
        start_x = 45
        y = 215

        cards = [
            ("Repos", stats.repositories),
            ("Stars", stats.stars),
            ("Forks", stats.forks),
            ("Followers", stats.followers),
            ("Following", stats.following),
        ]

        for i, (title, value) in enumerate(cards):
            c.stat_card(
                x=start_x + i * (card_width + gap),
                y=y,
                width=card_width,
                height=card_height,
                title=title,
                value=str(value),
                background=self.colors["background"],
                border=self.colors["border"],
                title_color=self.colors["secondary"],
                value_color=self.colors["title"],
            )

        # Technologies
        c.text(
            610,
            195,
            "Technologies",
            size=18,
            fill=self.colors["title"],
            weight="bold",
        )

        x = 610
        y = 220

        for tech in PROFILE.technologies:
            c.badge(
                x=x,
                y=y,
                text=tech,
                background=self.colors["background"],
                color=self.colors["text"],
                border=self.colors["border"],
            )

            x += len(tech) * 8 + 38

            if x > 810:
                x = 610
                y += 40

        # Footer
        c.line(
            45,
            315,
            855,
            315,
            self.colors["border"],
        )

        c.text(
            45,
            340,
            f"Auto-generated • Updated: {current_timestamp()}",
            size=12,
            fill=self.colors["secondary"],
        )

        c.save(output_file)