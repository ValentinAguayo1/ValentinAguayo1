from unittest.mock import MagicMock, patch
from github_api import GitHubAPI
from models import GitHubStats


@patch.dict("os.environ", {"GH_TOKEN": "token_falso_de_prueba"})
@patch("github_api.requests.post")
def test_get_basic_profile_exito(mock_post):
    """Verifica la respuesta exitosa simulando GraphQL."""
    # 1. Creamos la respuesta simulada que respondería GitHub GraphQL
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "user": {
                "repositories": {"totalCount": 12},
                "followers": {"totalCount": 45},
                "following": {"totalCount": 10},
            }
        }
    }
    mock_post.return_value = mock_response

    # 2. Instanciamos y ejecutamos
    api = GitHubAPI()
    stats = api.get_basic_profile()

    # 3. Aserciones
    assert isinstance(stats, GitHubStats)
    assert stats.repositories == 12
    assert stats.followers == 45
    assert stats.following == 10
    mock_post.assert_called_once()


@patch.dict("os.environ", {"GH_TOKEN": "token_falso_de_prueba"})
@patch("github_api.requests.post")
def test_get_basic_profile_graphql_error(mock_post):
    """Verifica que si GraphQL responde con la clave 'errors', la API use el fallback sin romper."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "errors": [{"message": "User not found"}]
    }
    mock_post.return_value = mock_response

    api = GitHubAPI()
    stats = api.get_basic_profile()
    assert stats.repositories == 0
    assert stats.followers == 0
    assert stats.following == 0


@patch.dict("os.environ", {}, clear=True)
def test_get_basic_profile_sin_token():
    """Verifica que si no hay GH_TOKEN en las variables de entorno, retorne los datos fallback."""
    api = GitHubAPI()
    stats = api.get_basic_profile()

    assert stats.repositories == 0
    assert stats.followers == 0
    assert stats.following == 0