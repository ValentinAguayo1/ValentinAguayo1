from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileConfig:
    username: str
    name: str
    role: str
    location: str
    bio: str
    technologies: list[str]


PROFILE = ProfileConfig(
    username="ValentinAguayo1",
    name="Valentín Aguayo",
    role="Computer Science Student",
    location="🇨🇱 Chile",
    bio="Backend developer in progress. Passionate about Python, Java and software engineering.",
    technologies=[
        "Python",
        "Java",
        "C#",
        "Git",
        "GitHub",
        "VS Code",
    ],
)


THEMES = {
    "dark": {
        "background": "#0d1117",
        "card": "#161b22",
        "border": "#30363d",
        "title": "#58a6ff",
        "text": "#c9d1d9",
        "secondary": "#8b949e",
        "accent": "#3fb950",
    },
    "light": {
        "background": "#ffffff",
        "card": "#f6f8fa",
        "border": "#d0d7de",
        "title": "#0969da",
        "text": "#24292f",
        "secondary": "#57606a",
        "accent": "#1a7f37",
    },
}