import os
from collections import defaultdict
from datetime import datetime, timezone

import requests

from config import LANGUAGE_COLORS, PROFILE
from models import GitHubStats, Language
from utils import percentage

GRAPHQL_URL = "https://api.github.com/graphql"


class GitHubAPI:
    def __init__(self):
        self.token = os.getenv("GH_TOKEN")

        self.headers = {
            "Authorization": f"Bearer {self.token}" if self.token else "",
            "Content-Type": "application/json",
        }

    def execute(self, query: str, variables: dict | None = None) -> dict:
        if not self.token:
            print(
                "[Warning] No existe la variable GH_TOKEN. Se usará respuesta por defecto."
            )
            raise RuntimeError("GH_TOKEN no configurado")

        try:
            response = requests.post(
                GRAPHQL_URL,
                json={
                    "query": query,
                    "variables": variables or {},
                },
                headers=self.headers,
                timeout=15,
            )

            if response.status_code in (403, 429):
                print("[Warning] Rate limit alcanzado en GitHub GraphQL API.")
                raise RuntimeError("Rate limit alcanzado")

            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"[Error] GraphQL devolvió errores: {data['errors']}")
                raise RuntimeError("Errores en la consulta GraphQL")

            return data.get("data", {})

        except (requests.exceptions.RequestException, RuntimeError) as err:
            print(f"[Error] Falló la ejecución en GitHubAPI: {err}")
            raise

    def get_basic_profile(self) -> GitHubStats:
        now = datetime.now(timezone.utc)
        year_start = datetime(now.year, 1, 1, tzinfo=timezone.utc)

        query = """
        query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            avatarUrl
            url
            followers {
              totalCount
            }
            contributionsCollection(from: $from, to: $to) {
              totalCommitContributions
              totalPullRequestContributions
              totalIssueContributions
            }
            repositories(ownerAffiliations: OWNER, first: 100, isFork: false) {
              totalCount
              nodes {
                stargazerCount
                forkCount
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges {
                    size
                    node {
                      name
                      color
                    }
                  }
                }
              }
            }
          }
        }
        """

        try:
            data = self.execute(
                query,
                {
                    "login": PROFILE.username,
                    "from": year_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "to": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
            )

            user = data.get("user") or {}
            repos = user.get("repositories") or {}
            nodes = repos.get("nodes") or []
            contrib = user.get("contributionsCollection") or {}

            stars = sum(n.get("stargazerCount", 0) for n in nodes)
            forks = sum(n.get("forkCount", 0) for n in nodes)
            languages = self._aggregate_languages(nodes)

            return GitHubStats(
                repositories=repos.get("totalCount", 0),
                followers=user.get("followers", {}).get("totalCount", 0),
                stars=stars,
                forks=forks,
                commits=contrib.get("totalCommitContributions", 0),
                pull_requests=contrib.get("totalPullRequestContributions", 0),
                issues=contrib.get("totalIssueContributions", 0),
                avatar_url=user.get("avatarUrl", ""),
                profile_url=user.get("url", ""),
                languages=languages,
            )

        except (requests.exceptions.RequestException, RuntimeError) as e:
            print(
                f"[Fallback] Generando GitHubStats por defecto debido a un error: {e}"
            )
            return GitHubStats()

    @staticmethod
    def _aggregate_languages(nodes: list) -> list[Language]:
        sizes: dict[str, int] = defaultdict(int)
        colors: dict[str, str] = {}

        for node in nodes:
            edges = (node.get("languages") or {}).get("edges") or []
            for edge in edges:
                lang = edge.get("node") or {}
                name = lang.get("name")
                if not name:
                    continue
                sizes[name] += edge.get("size", 0)
                colors[name] = lang.get("color") or LANGUAGE_COLORS.get(
                    name, "#2DD4BF"
                )

        total = sum(sizes.values())
        ranked = sorted(sizes.items(), key=lambda item: item[1], reverse=True)[:5]

        return [
            Language(
                name=name,
                percentage=percentage(size, total),
                color=colors.get(name, LANGUAGE_COLORS.get(name, "#2DD4BF")),
            )
            for name, size in ranked
        ]
