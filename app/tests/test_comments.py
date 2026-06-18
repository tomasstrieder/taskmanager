def test_create_comment(client, headers, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"content": "Test comment"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Test comment"
    assert "id" in data
    assert "user" in data


def test_create_comment_no_auth(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"content": "Test comment"},
    )
    assert response.status_code == 401


def test_create_comment_empty_content(client, headers, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"content": "   "},
        headers=headers,
    )
    assert response.status_code == 422


def test_create_comment_task_not_found(client, headers):
    response = client.post(
        "/tasks/99999/comments",
        json={"content": "Test comment"},
        headers=headers,
    )
    assert response.status_code == 404


def test_list_comments(client, headers, created_task, created_comment):
    response = client.get(f"/tasks/{created_task['id']}/comments", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["content"] == "Test comment"


def test_list_comments_task_not_found(client, headers):
    response = client.get("/tasks/99999/comments", headers=headers)
    assert response.status_code == 404


def test_delete_comment(client, headers, created_comment):
    response = client.delete(f"/comments/{created_comment['id']}", headers=headers)
    assert response.status_code == 200


def test_delete_comment_wrong_user(client, created_comment, headers2):
    response = client.delete(f"/comments/{created_comment['id']}", headers=headers2)
    assert response.status_code == 403


def test_delete_comment_not_found(client, headers):
    response = client.delete("/comments/99999", headers=headers)
    assert response.status_code == 404
