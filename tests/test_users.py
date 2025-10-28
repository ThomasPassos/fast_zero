from http import HTTPStatus

from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "username": "Thomas",
            "email": "tm123br@live.com",
            "password": "bololo",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "Thomas",
        "email": "tm123br@live.com",
        "id": 1,
    }


def test_create_user_with_same_username(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "username": "Thomas",
            "email": "tm123br@live.com",
            "password": "bololo",
        },
    )

    response = client.post(
        "/users/",
        json={
            "username": "Thomas",
            "email": "bololo@live.com",
            "password": "bololo",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_with_same_email(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "username": "Thomas",
            "email": "tm123br@live.com",
            "password": "bololo",
        },
    )

    response = client.post(
        "/users/",
        json={
            "username": "bololo",
            "email": "tm123br@live.com",
            "password": "bololo",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_user(client: TestClient, user):
    from fast_zero.schemas import UserPublic  # noqa: PLC0415

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_users(client: TestClient, user, token):
    from fast_zero.schemas import UserPublic  # noqa: PLC0415

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client: TestClient, user, token):
    response = client.put(
        f"/users/{user.id}",
        json={
            "username": "Bob",
            "email": "bob@example.com",
            "password": "secret",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "Bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_delete_user(client: TestClient, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}
