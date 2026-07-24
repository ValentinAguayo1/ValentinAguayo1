from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Language:
    name: str
    percentage: float
    color: str = "#58A6FF"


@dataclass(slots=True)
class GitHubStats:
    repositories: int = 0
    followers: int = 0
    following: int = 0

    stars: int = 0
    forks: int = 0

    commits: int = 0
    contributions: int = 0

    pull_requests: int = 0
    issues: int = 0

    avatar_url: str = ""
    profile_url: str = ""

    created_at: str = ""

    languages: list[Language] = field(default_factory=list)

    updated_at: datetime = field(default_factory=datetime.utcnow)