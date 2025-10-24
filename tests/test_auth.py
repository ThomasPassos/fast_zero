from http import HTTPStatus


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
