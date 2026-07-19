from github_api import obtener_estadisticas
from svg_renderer import generar


def main():

    stats = obtener_estadisticas()

    generar("dark", stats)
    generar("light", stats)

    print("SVGs generados correctamente.")


if __name__ == "__main__":
    main()