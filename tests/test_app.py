from http import HTTPStatus

from fastapi.testclient import TestClient


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_hello_world_deve_retornar_ok_e_ola_mundo(client: TestClient):
    response = client.get("/hello_world")

    assert response.status_code == HTTPStatus.OK
    assert response.text == "<h1>Olá Mundo!</h1>"


def test_get_token(client, user, token):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
        headers={"Authorization": f"Bearer {token}"},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
