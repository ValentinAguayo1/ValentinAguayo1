from github_api import GitHubAPI
from svg_renderer import SVGRenderer


def main():
    print("Obteniendo datos de GitHub...")

    api = GitHubAPI()
    stats = api.get_basic_profile()

    print("Generando tema oscuro...")
    SVGRenderer("dark").render(stats, "dark_mode.svg")

    print("Generando tema claro...")
    SVGRenderer("light").render(stats, "light_mode.svg")

    print("¡Archivos generados correctamente!")


if __name__ == "__main__":
    main()