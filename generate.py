from pathlib import Path

from github_api import GitHubAPI
from svg import BannerRenderer, StatsRenderer, StreakRenderer

OUTPUT = {
    "dark": ("dark_mode.svg", "streak_dark.svg", "stats_dark.svg"),
    "light": ("light_mode.svg", "streak_light.svg", "stats_light.svg"),
}


def render_all(stats, output_dir: Path | str = "."):
    dest = Path(output_dir)
    for theme, (banner, streak, stats_file) in OUTPUT.items():
        BannerRenderer(theme).render(stats, str(dest / banner))
        StreakRenderer(theme).render(stats, str(dest / streak))
        StatsRenderer(theme).render(stats, str(dest / stats_file))


def main():
    print("Fetching GitHub stats...")
    render_all(GitHubAPI().get_basic_profile())
    print("Wrote light/dark SVG files.")


if __name__ == "__main__":
    main()
