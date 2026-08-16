from pathlib import Path

from models import GitHubStats, Language
from svg_renderer import SVGRenderer, StreakRenderer


def test_renderer_smoke(tmp_path: Path):
    stats = GitHubStats(
        repositories=4,
        followers=5,
        stars=3,
        forks=1,
        commits=42,
        pull_requests=7,
        issues=3,
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
    assert "42 commits" in content
    assert "7 PRs" in content
    assert "3 issues" in content
    assert "Building APIs" in content


def test_streak_renderer_smoke(tmp_path: Path):
    stats = GitHubStats(
        contributions=54,
        current_streak=14,
        longest_streak=14,
        current_streak_range="Jul 29 - Aug 11",
        longest_streak_range="Jul 29 - Aug 11",
        created_at="2022-10-13T14:06:45Z",
    )
    out = tmp_path / "streak.svg"
    StreakRenderer("dark").render(stats, str(out))
    content = out.read_text(encoding="utf-8")
    assert "Current Streak" in content
    assert "14" in content
    assert "54" in content
    assert "Streak updates on the next Actions run" not in content
