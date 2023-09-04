import pytest
import requests
import yaml
from ddt import ddt, data, unpack

@pytest.fixture(scope="session")
def site_url():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config["site_url"]

@ddt
@pytest.mark.parametrize("header_value", ["X-Auth-Token", "Bearer token", "Invalid token"])
def test_posts(auth_token, site_url, header_value):
    url = f"{site_url}/api/posts"
    headers = {
        "X-Auth-Token": auth_token,
    }
    params = {"owner": "notMe"}

    response = requests.get(url, headers=headers, params=params)

    assert response.status_code == 200, "Failed to retrieve posts"
    posts = response.json().get("posts")
    assert posts, "No posts found in response"


    # Новый тест для создания и проверки нового поста
    def test_create_and_verify_post(auth_token, site_url):
        url = f"{site_url}/api/posts"
        headers = {
            "X-Auth-Token": auth_token,
        }
        payload = {
            "description": "Test post",
        }

        # Создаем новый пост
        response = requests.post(url, headers=headers, json=payload)

        assert response.status_code == 201, "Failed to create a new post"
        new_post_id = response.json().get("id")
        assert new_post_id, "New post ID not found in response"

        # Проверяем наличие созданного поста по описанию
        response = requests.get(url, headers=headers, params={"description": payload["description"]})

        assert response.status_code == 200, "Failed to retrieve posts"
        posts = response.json().get("posts")

        # Проверяем, что созданный пост с указанным описанием есть в списке постов
        assert any(post["id"] == new_post_id for post in posts), "New post not found in response"