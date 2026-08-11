from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FeaturedProject:
    name: str
    url: str
    blurb: str
    stack: str
    demo: str = ""


@dataclass(frozen=True, slots=True)
class ProfileConfig:
    username: str
    name: str
    role: str
    location: str
    tagline: str
    stack_line: str


PROFILE = ProfileConfig(
    username="ValentinAguayo1",
    name="Valentín Aguayo",
    role="Systems builder",
    location="Chile",
    tagline="Building APIs, CLIs, and systems that stay maintainable",
    stack_line="Chile · Python · TypeScript · Java · C#",
)

FEATURED_PROJECTS = [
    FeaturedProject(
        name="TaskFlow",
        url="https://github.com/ValentinAguayo1/taskflow",
        blurb="Task manager with Focus mode — answers “what should I do now?”",
        stack="Angular · Firebase · Firestore",
        demo="https://taskflow-878df.web.app",
    ),
    FeaturedProject(
        name="gh-summary-cli",
        url="https://github.com/ValentinAguayo1/gh-summary-cli",
        blurb="Python CLI for GitHub profiles, repo health audits, and Gemini summaries",
        stack="Python · Typer · Rich · httpx · Gemini",
    ),
]

# Language colors for the SVG bar (subset; unknown names fall back to accent)
LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#3178C6",
    "JavaScript": "#F1E05A",
    "Java": "#B07219",
    "C#": "#178600",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "SCSS": "#C6538C",
    "Shell": "#89E051",
}

THEMES = {
    "dark": {
        "background": "#0B1220",
        "surface": "#121A2B",
        "border": "#243049",
        "title": "#E8EEF7",
        "text": "#B8C4D6",
        "secondary": "#7A8BA3",
        "accent": "#2DD4BF",
        "bar_track": "#1A2438",
    },
    "light": {
        "background": "#F4F7FB",
        "surface": "#FFFFFF",
        "border": "#D5DEEB",
        "title": "#0F1B2D",
        "text": "#334155",
        "secondary": "#64748B",
        "accent": "#0F766E",
        "bar_track": "#E2E8F0",
    },
}
