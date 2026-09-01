import os
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

import requests

from config import PROFILE

GRAPHQL_URL = "https://api.github.com/graphql"
FALLBACK_LANG_COLOR = "#2DD4BF"


@dataclass(slots=True)
class Language:
    name: str
    percentage: float
    color: str = "#58A6FF"


@dataclass(slots=True)
class GitHubStats:
    repositories: int = 0
    followers: int = 0
    stars: int = 0
    commits: int = 0
    contributions: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    current_streak_range: str = ""
    longest_streak_range: str = ""
    pull_requests: int = 0
    issues: int = 0
    languages: list[Language] = field(default_factory=list)


def _percentage(value: int, total: int) -> float:
    return 0.0 if total <= 0 else round((value / total) * 100, 1)


class GitHubAPI:
    def __init__(self):
        self.token = os.getenv("GH_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}" if self.token else "",
            "Content-Type": "application/json",
        }

    def get_basic_profile(self) -> GitHubStats:
        if not self.token:
            print("GH_TOKEN missing; writing empty stats.")
            return GitHubStats()

        now = datetime.now(timezone.utc)
        query = """
        query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            followers { totalCount }
            contributionsCollection(from: $from, to: $to) {
              totalCommitContributions
              totalPullRequestContributions
              totalIssueContributions
              contributionCalendar {
                totalContributions
                weeks { contributionDays { date contributionCount } }
              }
            }
            repositories(ownerAffiliations: OWNER, first: 100, isFork: false) {
              totalCount
              nodes {
                stargazerCount
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size node { name color } }
                }
              }
            }
          }
        }
        """
        try:
            response = requests.post(
                GRAPHQL_URL,
                json={
                    "query": query,
                    "variables": {
                        "login": PROFILE.username,
                        "from": datetime(now.year, 1, 1, tzinfo=timezone.utc).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "to": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    },
                },
                headers=self.headers,
                timeout=15,
            )
            if response.status_code in (403, 429):
                raise RuntimeError("GitHub rate limit")
            response.raise_for_status()
            payload = response.json()
            if payload.get("errors"):
                raise RuntimeError(payload["errors"])
            user = (payload.get("data") or {}).get("user") or {}
            repos = user.get("repositories") or {}
            nodes = repos.get("nodes") or []
            contrib = user.get("contributionsCollection") or {}
            calendar = contrib.get("contributionCalendar") or {}
            streak = self._streaks_from_calendar(calendar)
            return GitHubStats(
                repositories=repos.get("totalCount", 0),
                followers=user.get("followers", {}).get("totalCount", 0),
                stars=sum(n.get("stargazerCount", 0) for n in nodes),
                commits=contrib.get("totalCommitContributions", 0),
                contributions=calendar.get("totalContributions", 0) or streak[0],
                current_streak=streak[1],
                longest_streak=streak[2],
                current_streak_range=streak[3],
                longest_streak_range=streak[4],
                pull_requests=contrib.get("totalPullRequestContributions", 0),
                issues=contrib.get("totalIssueContributions", 0),
                languages=self._aggregate_languages(nodes),
            )
        except (requests.exceptions.RequestException, RuntimeError) as err:
            print(f"GitHub fetch failed ({err}); writing empty stats.")
            return GitHubStats()

    @staticmethod
    def _format_range(start: date, end: date) -> str:
        if start == end:
            return start.strftime("%b %d")
        if start.year == end.year:
            return f"{start.strftime('%b %d')} - {end.strftime('%b %d')}"
        return f"{start.strftime('%b %d, %Y')} - {end.strftime('%b %d, %Y')}"

    @classmethod
    def _streaks_from_calendar(
        cls,
        calendar: dict,
        today: date | None = None,
    ) -> tuple[int, int, int, str, str]:
        today = today or datetime.now(timezone.utc).date()
        counts: dict[date, int] = {}
        for week in calendar.get("weeks") or []:
            for day in week.get("contributionDays") or []:
                raw = day.get("date")
                if not raw:
                    continue
                try:
                    parsed = date.fromisoformat(raw[:10])
                except ValueError:
                    continue
                counts[parsed] = int(day.get("contributionCount") or 0)

        total = int(calendar.get("totalContributions") or sum(counts.values()))
        if not counts:
            return total, 0, 0, "", ""

        contrib_days = sorted(d for d, n in counts.items() if n > 0)
        longest = 0
        longest_start = longest_end = None
        run = 0
        run_start = None
        prev = None
        for d in contrib_days:
            if prev is not None and d == prev + timedelta(days=1):
                run += 1
            else:
                run = 1
                run_start = d
            if run > longest:
                longest = run
                longest_start, longest_end = run_start, d
            prev = d

        cursor = today if counts.get(today, 0) > 0 else today - timedelta(days=1)
        current = 0
        current_start = current_end = None
        while counts.get(cursor, 0) > 0:
            if current_end is None:
                current_end = cursor
            current_start = cursor
            current += 1
            cursor -= timedelta(days=1)

        current_range = (
            cls._format_range(current_start, current_end)
            if current and current_start and current_end
            else ""
        )
        longest_range = (
            cls._format_range(longest_start, longest_end)
            if longest_start and longest_end
            else ""
        )
        return total, current, longest, current_range, longest_range

    @staticmethod
    def _aggregate_languages(nodes: list) -> list[Language]:
        sizes: dict[str, int] = defaultdict(int)
        colors: dict[str, str] = {}
        for node in nodes:
            for edge in (node.get("languages") or {}).get("edges") or []:
                lang = edge.get("node") or {}
                name = lang.get("name")
                if not name:
                    continue
                sizes[name] += edge.get("size", 0)
                colors[name] = lang.get("color") or FALLBACK_LANG_COLOR
        total = sum(sizes.values())
        ranked = sorted(sizes.items(), key=lambda item: item[1], reverse=True)[:5]
        return [
            Language(
                name=name,
                percentage=_percentage(size, total),
                color=colors.get(name, FALLBACK_LANG_COLOR),
            )
            for name, size in ranked
        ]
