from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
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
        "background": "#0D1117",
        "card": "#161B22",
        "border": "#30363D",
        "title": "#58A6FF",
        "text": "#C9D1D9",
        "secondary": "#8B949E",
        "accent": "#3FB950",
    },
    "light": {
        "background": "#FFFFFF",
        "card": "#F6F8FA",
        "border": "#D0D7DE",
        "title": "#0969DA",
        "text": "#24292F",
        "secondary": "#57606A",
        "accent": "#1A7F37",
    },
}