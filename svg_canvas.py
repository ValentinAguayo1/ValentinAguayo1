from pathlib import Path


FONT = (
    "ui-monospace, Cascadia Code, Cascadia Mono, Segoe UI Mono, "
    "Consolas, Liberation Mono, Menlo, monospace"
)


class SVGCanvas:
    def __init__(self, width: int, height: int, background: str):
        self.width = width
        self.height = height
        self.background = background
        self.elements: list[str] = []
        self._defs: list[str] = []

    def add_def(self, content: str):
        self._defs.append(content)

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
        extra: str = "",
    ):
        attrs = (
            f'x="{x}" y="{y}" '
            f'width="{width}" height="{height}" '
            f'fill="{fill}" '
            f'stroke="{stroke}" '
            f'stroke-width="{stroke_width}" '
            f'rx="{rx}"'
        )
        if extra:
            attrs = f"{attrs} {extra}"
        self.elements.append(f"<rect {attrs}/>")

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
        children: str = "",
    ):
        spacing = (
            f' letter-spacing="{letter_spacing}"' if letter_spacing is not None else ""
        )
        attrs = (
            f'x="{x}" y="{y}" '
            f'font-family="{FONT}" '
            f'font-size="{size}" '
            f'font-weight="{weight}" '
            f'fill="{fill}"{spacing}'
        )
        if extra:
            attrs = f"{attrs} {extra}"
        escaped = (
            content.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        self.elements.append(f"<text {attrs}>{children}{escaped}</text>")

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str,
        width: float = 1,
        extra: str = "",
    ):
        attrs = (
            f'x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" '
            f'stroke="{color}" '
            f'stroke-width="{width}"'
        )
        if extra:
            attrs = f"{attrs} {extra}"
        self.elements.append(f"<line {attrs}/>")

    def language_bar(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        segments: list[tuple[str, float]],
        track: str,
    ):
        """segments: list of (color, fraction 0-1)."""
        self.rect(x, y, width, height, fill=track, rx=height / 2)

        offset = 0.0
        for i, (color, fraction) in enumerate(segments):
            if fraction <= 0:
                continue
            seg_w = width * fraction
            if offset + seg_w > width:
                seg_w = width - offset
            if seg_w <= 0:
                break

            begin = f"{0.35 + i * 0.08}s"
            self.raw(
                f'<rect x="{x + offset}" y="{y}" width="{seg_w:.2f}" height="{height}" '
                f'fill="{color}" rx="{height / 2 if i == 0 else 0}">'
                f'<animate attributeName="width" from="0" to="{seg_w:.2f}" '
                f'dur="0.7s" begin="{begin}" fill="freeze"/>'
                f"</rect>"
            )
            offset += seg_w

    def build(self) -> str:
        defs = ""
        if self._defs:
            defs = "<defs>\n" + "\n".join(self._defs) + "\n</defs>\n"

        body = "\n".join(self.elements)

        return f"""<svg
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink"
width="{self.width}"
height="{self.height}"
viewBox="0 0 {self.width} {self.height}"
role="img"
aria-label="Valentín Aguayo profile banner">

{defs}<rect width="100%" height="100%" fill="{self.background}"/>

{body}

</svg>
"""

    def save(self, filename: str):
        Path(filename).write_text(
            self.build(),
            encoding="utf-8",
        )
