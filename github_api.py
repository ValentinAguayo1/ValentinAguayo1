import os
import requests

from config import PROFILE


GITHUB_GRAPHQL = "https://api.github.com/graphql"


class GitHubAPI:

    def __init__(self):

        token = os.getenv("GH_TOKEN")

        if token is None:
            raise RuntimeError(
                "No existe GH_TOKEN."
            )

        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    def execute(self, query: str):

        response = requests.post(
            GITHUB_GRAPHQL,
            json={"query": query},
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        body = response.json()

        if "errors" in body:
            raise RuntimeError(body["errors"])

        return body["data"]
    

    def get_basic_profile(self):
        query = f"""
        {{
          user(login: "{PROFILE.username}") {{
            name

            followers {{
              totalCount
            }}

            following {{
              totalCount
            }}

            repositories(ownerAffiliations: OWNER) {{
              totalCount
            }}
          }}
        }}
        """

        return self.execute(query)