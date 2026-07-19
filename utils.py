from typing import Dict


def abbreviate(number: int) -> str:
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"

    if number >= 1_000:
        return f"{number / 1_000:.1f}K"

    return str(number)


def percentage(value: int, total: int) -> float:
    if total == 0:
        return 0

    return round((value / total) * 100, 1)


def top_languages(languages: Dict[str, int], limit: int = 5):
    return sorted(
        languages.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:limit]