from pathlib import Path

from models import GitHubStats, Language
from svg_renderer import SVGRenderer


def test_renderer_smoke(tmp_path: Path):
    stats = GitHubStats(
        repositories=4,
        followers=5,
        stars=3,
        forks=1,
        languages=[
            Language(name="Python", percentage=60.0, color="#3572A5"),
            Language(name="TypeScript", percentage=40.0, color="#3178C6"),
        ],
    )

    out = tmp_path / "banner.svg"
    SVGRenderer("dark").render(stats, str(out))

    content = out.read_text(encoding="utf-8")
    assert "Valentín Aguayo".upper() in content or "VALENTÍN AGUAYO" in content
    assert "Following" not in content
    assert "languages" in content
    assert "4 repos" in content
    assert "Building APIs" in content
