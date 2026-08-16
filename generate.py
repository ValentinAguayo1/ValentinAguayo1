from github_api import GitHubAPI
from svg_renderer import SVGRenderer, StreakRenderer, StatsRenderer


def main():
    print("Obteniendo datos de GitHub...")

    api = GitHubAPI()
    stats = api.get_basic_profile()

    print("Generando tema oscuro...")
    SVGRenderer("dark").render(stats, "dark_mode.svg")
    StreakRenderer("dark").render(stats, "streak_dark.svg")
    StatsRenderer("dark").render(stats, "stats_dark.svg")

    print("Generando tema claro...")
    SVGRenderer("light").render(stats, "light_mode.svg")
    StreakRenderer("light").render(stats, "streak_light.svg")
    StatsRenderer("light").render(stats, "stats_light.svg")

    print("¡Archivos generados correctamente!")


if __name__ == "__main__":
    main()
