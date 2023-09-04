import pytest
import requests
import yaml

@pytest.fixture(scope="session")
def auth_token():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    login_url = f"{config['site_url']}/gateway/login"
    payload = {
        "username": config["username"],
        "password": config["password"],
    }

    response = requests.post(login_url, json=payload)
    assert response.status_code == 200, "Authentication failed"

    token = response.json().get("token")
    assert token, "Token not found in response"

    return token