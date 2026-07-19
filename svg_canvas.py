from pathlib import Path


class SVGCanvas:
    def __init__(self, width: int, height: int, background: str):
        self.width = width
        self.height = height
        self.background = background
        self.elements = []

    def rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        fill: str,
        stroke: str = "none",
        stroke_width: int = 0,
        rx: int = 0,
    ):
        self.elements.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}" rx="{rx}"/>'
        )

    def text(
        self,
        x: int,
        y: int,
        content: str,
        size: int = 18,
        fill: str = "#FFFFFF",
        weight: str = "normal",
    ):
        self.elements.append(
            f'<text x="{x}" y="{y}" '
            f'font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="{size}" '
            f'font-weight="{weight}" '
            f'fill="{fill}">{content}</text>'
        )

    def line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str,
        width: int = 1,
    ):
        self.elements.append(
            f'<line x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="{color}" '
            f'stroke-width="{width}"/>'
        )

    def build(self) -> str:
        body = "\n".join(self.elements)

        return f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{self.width}"
height="{self.height}"
viewBox="0 0 {self.width} {self.height}">

<rect width="100%" height="100%" fill="{self.background}"/>

{body}

</svg>
"""

    def save(self, filename: str):
        Path(filename).write_text(
            self.build(),
            encoding="utf-8",
        )