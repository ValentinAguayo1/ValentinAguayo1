from datetime import datetime, timezone


def format_number(value: int) -> str:
    """
    Formatea un número con separadores de miles.
    """
    return f"{value:,}"


def current_timestamp() -> str:
    """
    Devuelve la fecha y hora actual en formato UTC.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Limita un valor entre un mínimo y un máximo.
    """
    return max(minimum, min(value, maximum))


def percentage(value: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((value / total) * 100, 1)


def _exponential_cdf(x: float) -> float:
    return 1 - 2 ** -x


def _log_normal_cdf(x: float) -> float:
    return x / (1 + x)


def calculate_rank(
    *,
    commits: int,
    pull_requests: int,
    issues: int,
    stars: int,
    followers: int,
    reviews: int = 0,
) -> tuple[str, float]:
    """
    Rank in the style of github-readme-stats (percentile of typical activity).
    Returns (letter, percentile 0-100) where lower percentile is stronger.
    """
    weights = {
        "commits": 2,
        "prs": 3,
        "issues": 1,
        "reviews": 1,
        "stars": 4,
        "followers": 1,
    }
    total_weight = sum(weights.values())
    score = (
        weights["commits"] * _exponential_cdf(commits / 250)
        + weights["prs"] * _exponential_cdf(pull_requests / 50)
        + weights["issues"] * _exponential_cdf(issues / 25)
        + weights["reviews"] * _exponential_cdf(reviews / 2)
        + weights["stars"] * _log_normal_cdf(stars / 50)
        + weights["followers"] * _log_normal_cdf(followers / 10)
    ) / total_weight
    percentile = (1 - score) * 100

    thresholds = (
        (1, "S"),
        (12.5, "A+"),
        (25, "A"),
        (37.5, "A-"),
        (50, "B+"),
        (62.5, "B"),
        (75, "B-"),
        (87.5, "C+"),
        (100, "C"),
    )
    letter = "C"
    for limit, name in thresholds:
        if percentile <= limit:
            letter = name
            break
    return letter, round(percentile, 1)
