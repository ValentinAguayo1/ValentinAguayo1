from datetime import date
from pathlib import Path

from generate import render_all
from github_api import GitHubAPI, GitHubStats, Language


def test_render_all_generates_expected_files(tmp_path: Path):
    stats = GitHubStats(
        repositories=4,
        followers=5,
        stars=3,
        commits=42,
        pull_requests=7,
        issues=1,
        languages=[
            Language(name="Python", percentage=52.4, color="#3572A5"),
            Language(name="TypeScript", percentage=16.4, color="#3178C6"),
            Language(name="SCSS", percentage=14.9, color="#c6538c"),
            Language(name="HTML", percentage=10.1, color="#e34c26"),
            Language(name="CSS", percentage=3.5, color="#663399"),
        ],
    )
    render_all(stats, tmp_path)
    banner = (tmp_path / "dark_mode.svg").read_text(encoding="utf-8")
    stats_svg = (tmp_path / "stats_dark.svg").read_text(encoding="utf-8")
    streak = (tmp_path / "streak_dark.svg").read_text(encoding="utf-8")
    for name in (
        "dark_mode.svg",
        "streak_dark.svg",
        "stats_dark.svg",
        "light_mode.svg",
        "streak_light.svg",
        "stats_light.svg",
    ):
        out = tmp_path / name
        assert out.exists()
        assert out.read_text(encoding="utf-8").startswith("<svg")
    assert "1 issue" in banner
    assert "1 issues" not in banner
    assert "CSS 3.5%" in banner
    assert "999999" not in banner
    assert "clipPath" in banner
    assert 'fill="#121A2B"' in stats_svg
    assert "GitHub stats" in stats_svg
    assert "2022 - Present" not in streak
    assert "Contributions" in streak


def test_streaks_from_calendar():
    calendar = {
        "totalContributions": 5,
        "weeks": [
            {
                "contributionDays": [
                    {"date": "2026-08-10", "contributionCount": 1},
                    {"date": "2026-08-11", "contributionCount": 2},
                    {"date": "2026-08-12", "contributionCount": 0},
                    {"date": "2026-08-13", "contributionCount": 1},
                    {"date": "2026-08-14", "contributionCount": 1},
                    {"date": "2026-08-15", "contributionCount": 1},
                ]
            }
        ],
    }
    total, current, longest, current_range, longest_range = (
        GitHubAPI._streaks_from_calendar(calendar, today=date(2026, 8, 15))
    )
    assert (total, current, longest) == (5, 3, 3)
    assert "Aug" in current_range and "Aug" in longest_range
