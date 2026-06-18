def test_create_user(client, user_payload):
    response = client.post("/users", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_payload["email"]
    assert data["name"] == user_payload["name"]
    assert "id" in data
    assert "hashed_password" not in data


def test_create_user_duplicate_email(client, created_user, user_payload):
    response = client.post("/users", json=user_payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_create_user_short_password(client):
    response = client.post("/users", json={
        "name": "Test",
        "email": "short@test.com",
        "password": "123",
    })
    assert response.status_code == 422


def test_create_user_invalid_email(client):
    response = client.post("/users", json={
        "name": "Test",
        "email": "not-an-email",
        "password": "123456",
    })
    assert response.status_code == 422


def test_get_user(client, created_user, headers):
    response = client.get(f"/users/{created_user['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == created_user["id"]


def test_get_user_not_found(client, headers):
    response = client.get("/users/99999", headers=headers)
    assert response.status_code == 404


def test_get_user_no_auth(client, created_user):
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == 401


def test_update_user_name(client, created_user, headers):
    response = client.put(
        f"/users/{created_user['id']}",
        json={"name": "Updated Name"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_user_other_user(client, created_user, headers2):
    response = client.put(
        f"/users/{created_user['id']}",
        json={"name": "Hacked"},
        headers=headers2,
    )
    assert response.status_code == 403


def test_delete_user(client, created_user, headers):
    response = client.delete(f"/users/{created_user['id']}", headers=headers)
    assert response.status_code == 200


def test_delete_user_other_user(client, created_user, headers2):
    response = client.delete(f"/users/{created_user['id']}", headers=headers2)
    assert response.status_code == 403


def test_get_deleted_user_returns_404(client, created_user, headers):
    client.delete(f"/users/{created_user['id']}", headers=headers)
    response = client.get(f"/users/{created_user['id']}", headers=headers)
    assert response.status_code == 401  # token is now invalid (user inactive)
