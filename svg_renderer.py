from datetime import datetime

from config import (
    NAME,
    ROLE,
    LOCATION,
    BIO,
    TECHNOLOGIES,
    THEMES,
)


WIDTH = 900
HEIGHT = 300


def generar(theme: str, stats: dict):

    colors = THEMES[theme]

    techs = " • ".join(TECHNOLOGIES)

    fecha = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">
<rect width="100%" height="100%" fill="{colors["background"]}"/>

<rect
    x="25"
    y="25"
    rx="18"
    width="850"
    height="250"
    fill="{colors["card"]}"
/>

<text
    x="50"
    y="70"
    font-size="28"
    font-family="Consolas, monospace"
    fill="{colors["title"]}"
    font-weight="bold">
{NAME}
</text>

<text
    x="50"
    y="100"
    font-size="18"
    font-family="Consolas"
    fill="{colors["text"]}">
{ROLE}
</text>

<text
    x="50"
    y="125"
    font-size="16"
    font-family="Consolas"
    fill="{colors["secondary"]}">
{LOCATION}
</text>

<text
    x="50"
    y="155"
    font-size="15"
    font-family="Consolas"
    fill="{colors["text"]}">
{BIO}
</text>

<text
    x="50"
    y="195"
    font-size="17"
    font-family="Consolas"
    fill="{colors["accent"]}">
Repositories : {stats["repositories"]}
</text>

<text
    x="300"
    y="195"
    font-size="17"
    font-family="Consolas"
    fill="{colors["accent"]}">
Followers : {stats["followers"]}
</text>

<text
    x="500"
    y="195"
    font-size="17"
    font-family="Consolas"
    fill="{colors["accent"]}">
Following : {stats["following"]}
</text>

<text
    x="50"
    y="230"
    font-size="15"
    font-family="Consolas"
    fill="{colors["secondary"]}">
{techs}
</text>

<text
    x="50"
    y="258"
    font-size="12"
    font-family="Consolas"
    fill="{colors["secondary"]}">
Updated automatically · {fecha}
</text>

</svg>
"""

    nombre = f"{theme}_mode.svg"

    with open(nombre, "w", encoding="utf-8") as archivo:
        archivo.write(svg)