from config import PROFILE, THEMES
from models import GitHubStats
from svg_canvas import SVGCanvas
from utils import current_timestamp


class SVGRenderer:
    WIDTH = 900
    HEIGHT = 320

    def __init__(self, theme: str):
        if theme not in THEMES:
            raise ValueError(f"Tema '{theme}' no válido.")

        self.colors = THEMES[theme]

        self.canvas = SVGCanvas(
            width=self.WIDTH,
            height=self.HEIGHT,
            background=self.colors["background"],
        )

    def render(self, stats: GitHubStats, output_file: str):
        c = self.canvas

        # Tarjeta principal
        c.rect(
            x=20,
            y=20,
            width=860,
            height=280,
            fill=self.colors["card"],
            stroke=self.colors["border"],
            stroke_width=1,
            rx=16,
        )

        # Título
        c.text(
            45,
            65,
            PROFILE.name,
            size=28,
            fill=self.colors["title"],
            weight="bold",
        )

        # Cargo
        c.text(
            45,
            95,
            PROFILE.role,
            size=16,
            fill=self.colors["secondary"],
        )

        # Línea separadora
        c.line(
            45,
            115,
            855,
            115,
            self.colors["border"],
        )

        # Estadísticas
        c.text(
            45,
            150,
            f"Repositories : {stats.repositories}",
            size=18,
            fill=self.colors["text"],
        )

        c.text(
            45,
            180,
            f"Followers    : {stats.followers}",
            size=18,
            fill=self.colors["text"],
        )

        c.text(
            45,
            210,
            f"Following    : {stats.following}",
            size=18,
            fill=self.colors["text"],
        )

        # Tecnologías
        c.text(
            450,
            150,
            "Technologies",
            size=20,
            fill=self.colors["title"],
            weight="bold",
        )

        y = 180

        for tech in PROFILE.technologies:
            c.text(
                450,
                y,
                f"• {tech}",
                size=18,
                fill=self.colors["text"],
            )
            y += 28

        # Footer
        c.line(
            45,
            265,
            855,
            265,
            self.colors["border"],
        )

        c.text(
            45,
            290,
            f"Updated: {current_timestamp()}",
            size=13,
            fill=self.colors["secondary"],
        )

        c.save(output_file)