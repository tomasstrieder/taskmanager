def test_login_success(client, created_user, user_payload):
    response = client.post("/auth/login", json={
        "email": user_payload["email"],
        "password": user_payload["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, created_user, user_payload):
    response = client.post("/auth/login", json={
        "email": user_payload["email"],
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_nonexistent_email(client):
    response = client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "123456",
    })
    assert response.status_code == 401


def test_logout(client, headers):
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200


def test_logout_without_token(client):
    response = client.post("/auth/logout")
    assert response.status_code == 401
