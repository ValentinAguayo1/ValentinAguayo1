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
            f'<rect x="{x}" y="{y}" '
            f'width="{width}" height="{height}" '
            f'fill="{fill}" '
            f'stroke="{stroke}" '
            f'stroke-width="{stroke_width}" '
            f'rx="{rx}"/>'
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

    def image(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        href: str,
        circular: bool = False,
    ):
        if circular:
            clip_id = f"clip_{len(self.elements)}"

            self.elements.append(
                f"""
<defs>
    <clipPath id="{clip_id}">
        <circle
            cx="{x + width / 2}"
            cy="{y + height / 2}"
            r="{min(width, height) / 2}"
        />
    </clipPath>
</defs>

<image
    x="{x}"
    y="{y}"
    width="{width}"
    height="{height}"
    xlink:href="{href}"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#{clip_id})"
/>
"""
            )
        else:
            self.elements.append(
                f"""
<image
    x="{x}"
    y="{y}"
    width="{width}"
    height="{height}"
    xlink:href="{href}"
    preserveAspectRatio="xMidYMid slice"
/>
"""
            )

    def avatar(
        self,
        x: int,
        y: int,
        size: int,
        href: str,
        border_color: str,
        border_width: int = 3,
    ):
        clip_id = f"avatar_clip_{len(self.elements)}"

        self.elements.append(
            f"""
<defs>
    <clipPath id="{clip_id}">
        <circle
            cx="{x + size / 2}"
            cy="{y + size / 2}"
            r="{size / 2}"
        />
    </clipPath>
</defs>

<circle
    cx="{x + size / 2}"
    cy="{y + size / 2}"
    r="{size / 2}"
    fill="none"
    stroke="{border_color}"
    stroke-width="{border_width}"
/>

<image
    x="{x}"
    y="{y}"
    width="{size}"
    height="{size}"
    xlink:href="{href}"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#{clip_id})"
/>
"""
        )

    def stat_card(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str,
        value: str,
        background: str,
        border: str,
        title_color: str,
        value_color: str,
    ):
        self.rect(
            x=x,
            y=y,
            width=width,
            height=height,
            fill=background,
            stroke=border,
            stroke_width=1,
            rx=12,
        )

        self.text(
            x + 15,
            y + 28,
            title,
            size=14,
            fill=title_color,
        )

        self.text(
            x + 15,
            y + 62,
            value,
            size=28,
            fill=value_color,
            weight="bold",
        )

    def badge(
        self,
        x: int,
        y: int,
        text: str,
        background: str,
        color: str,
        border: str,
    ):
        padding = 12
        height = 30
        width = len(text) * 8 + padding * 2

        self.rect(
            x=x,
            y=y,
            width=width,
            height=height,
            fill=background,
            stroke=border,
            stroke_width=1,
            rx=15,
        )

        self.text(
            x + padding,
            y + 20,
            text,
            size=14,
            fill=color,
            weight="bold",
        )

    def build(self) -> str:
        body = "\n".join(self.elements)

        return f"""<svg
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
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