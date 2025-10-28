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
