from datetime import datetime

template = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="250">

<rect width="100%" height="100%" fill="#0d1117"/>

<text x="50" y="70"
      font-size="36"
      fill="#58a6ff"
      font-family="Consolas">

Valentín Aguayo

</text>

<text x="50" y="120"
      font-size="22"
      fill="white"
      font-family="Consolas">

Computer Science Student

</text>

<text x="50" y="165"
      font-size="18"
      fill="#8b949e"
      font-family="Consolas">

Backend • Java • Python • C#

</text>

<text x="50" y="215"
      font-size="14"
      fill="#3fb950"
      font-family="Consolas">

Updated: {datetime.now().strftime("%d/%m/%Y %H:%M")}

</text>

</svg>
"""

with open("dark_mode.svg", "w", encoding="utf8") as f:
    f.write(template)

with open("light_mode.svg", "w", encoding="utf8") as f:
    f.write(
        template
        .replace("#0d1117", "white")
        .replace("white", "#24292f")
    )

print("SVG generado correctamente.")