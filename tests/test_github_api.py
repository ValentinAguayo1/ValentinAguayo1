from unittest.mock import MagicMock, patch

from github_api import GitHubAPI
from models import GitHubStats, Language


SAMPLE_GRAPHQL = {
    "data": {
        "user": {
            "avatarUrl": "https://avatars.githubusercontent.com/u/1",
            "url": "https://github.com/ValentinAguayo1",
            "followers": {"totalCount": 5},
            "contributionsCollection": {
                "totalCommitContributions": 42,
                "totalPullRequestContributions": 7,
                "totalIssueContributions": 3,
            },
            "repositories": {
                "totalCount": 4,
                "nodes": [
                    {
                        "stargazerCount": 2,
                        "forkCount": 1,
                        "languages": {
                            "edges": [
                                {
                                    "size": 800,
                                    "node": {"name": "Python", "color": "#3572A5"},
                                },
                                {
                                    "size": 200,
                                    "node": {
                                        "name": "TypeScript",
                                        "color": "#3178C6",
                                    },
                                },
                            ]
                        },
                    },
                    {
                        "stargazerCount": 1,
                        "forkCount": 0,
                        "languages": {
                            "edges": [
                                {
                                    "size": 500,
                                    "node": {
                                        "name": "TypeScript",
                                        "color": "#3178C6",
                                    },
                                },
                            ]
                        },
                    },
                ],
            },
        }
    }
}


@patch.dict("os.environ", {"GH_TOKEN": "token_falso_de_prueba"})
@patch("github_api.requests.post")
def test_get_basic_profile_exito(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = SAMPLE_GRAPHQL
    mock_post.return_value = mock_response

    api = GitHubAPI()
    stats = api.get_basic_profile()

    assert isinstance(stats, GitHubStats)
    assert stats.repositories == 4
    assert stats.followers == 5
    assert stats.stars == 3
    assert stats.forks == 1
    assert stats.commits == 42
    assert stats.pull_requests == 7
    assert stats.issues == 3
    assert stats.avatar_url.endswith("/u/1")
    assert len(stats.languages) >= 1
    assert stats.languages[0].name in {"Python", "TypeScript"}
    mock_post.assert_called_once()


@patch.dict("os.environ", {"GH_TOKEN": "token_falso_de_prueba"})
@patch("github_api.requests.post")
def test_get_basic_profile_graphql_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"errors": [{"message": "User not found"}]}
    mock_post.return_value = mock_response

    api = GitHubAPI()
    stats = api.get_basic_profile()
    assert stats.repositories == 0
    assert stats.followers == 0
    assert stats.stars == 0


@patch.dict("os.environ", {}, clear=True)
def test_get_basic_profile_sin_token():
    api = GitHubAPI()
    stats = api.get_basic_profile()

    assert stats.repositories == 0
    assert stats.followers == 0
    assert stats.stars == 0


def test_aggregate_languages():
    nodes = SAMPLE_GRAPHQL["data"]["user"]["repositories"]["nodes"]
    languages = GitHubAPI._aggregate_languages(nodes)

    assert isinstance(languages[0], Language)
    names = {lang.name for lang in languages}
    assert "Python" in names
    assert "TypeScript" in names
    assert abs(sum(lang.percentage for lang in languages) - 100.0) < 0.2
