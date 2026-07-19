import os
import requests

from config import PROFILE
from models import GitHubStats

GRAPHQL_URL = "https://api.github.com/graphql"


class GitHubAPI:
    def __init__(self):
        self.token = os.getenv("GH_TOKEN")

        if not self.token:
            raise RuntimeError("La variable de entorno GH_TOKEN no existe.")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def execute(self, query: str, variables: dict | None = None) -> dict:
        response = requests.post(
            GRAPHQL_URL,
            json={
                "query": query,
                "variables": variables or {},
            },
            headers=self.headers,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise RuntimeError(data["errors"])

        return data["data"]

    def get_basic_profile(self) -> GitHubStats:
        query = """
        query($login: String!) {
          user(login: $login) {
            followers {
              totalCount
            }

            following {
              totalCount
            }

            repositories(ownerAffiliations: OWNER) {
              totalCount
            }
          }
        }
        """

        data = self.execute(
            query,
            {
                "login": PROFILE.username,
            },
        )

        user = data["user"]

        return GitHubStats(
            repositories=user["repositories"]["totalCount"],
            followers=user["followers"]["totalCount"],
            following=user["following"]["totalCount"],
        )