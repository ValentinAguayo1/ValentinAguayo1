import os
import requests

from config import PROFILE
from models import GitHubStats

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
            print("[Warning] No existe la variable GH_TOKEN. Se usará respuesta por defecto.")
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

        try:
            data = self.execute(
                query,
                {
                    "login": PROFILE.username,
                },
            )

            user = data.get("user") or {}

            return GitHubStats(
                repositories=user.get("repositories", {}).get("totalCount", 0),
                followers=user.get("followers", {}).get("totalCount", 0),
                following=user.get("following", {}).get("totalCount", 0),
            )

        except Exception as e:
            print(f"[Fallback] Generando GitHubStats por defecto debido a un error: {e}")
            return GitHubStats(
                repositories=0,
                followers=0,
                following=0,
            )