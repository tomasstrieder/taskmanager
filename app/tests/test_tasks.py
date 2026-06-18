def test_create_task(client, headers):
    response = client.post("/tasks", json={"title": "My Task"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Task"
    assert "id" in data
    assert "creator" in data


def test_create_task_no_auth(client):
    response = client.post("/tasks", json={"title": "My Task"})
    assert response.status_code == 401


def test_create_task_missing_title(client, headers):
    response = client.post("/tasks", json={}, headers=headers)
    assert response.status_code == 422


def test_get_task(client, headers, created_task):
    response = client.get(f"/tasks/{created_task['id']}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert "creator" in data
    assert "comments" in data


def test_get_task_not_found(client, headers):
    response = client.get("/tasks/99999", headers=headers)
    assert response.status_code == 404


def test_list_tasks(client, headers, created_task):
    response = client.get("/tasks", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_list_tasks_filter_by_status(client, headers):
    client.post("/tasks", json={"title": "Todo Task",   "status": "todo"},        headers=headers)
    client.post("/tasks", json={"title": "Done Task",   "status": "done"},        headers=headers)
    client.post("/tasks", json={"title": "Active Task", "status": "in_progress"}, headers=headers)

    response = client.get("/tasks?status=todo", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["status"] == "todo" for t in tasks)


def test_list_tasks_filter_by_priority(client, headers):
    client.post("/tasks", json={"title": "High Task", "priority": "high"}, headers=headers)
    client.post("/tasks", json={"title": "Low Task",  "priority": "low"},  headers=headers)

    response = client.get("/tasks?priority=high", headers=headers)
    assert response.status_code == 200
    assert all(t["priority"] == "high" for t in response.json())


def test_update_task(client, headers, created_task):
    response = client.put(
        f"/tasks/{created_task['id']}",
        json={"title": "Updated Title", "status": "in_progress"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"


def test_update_task_not_found(client, headers):
    response = client.put("/tasks/99999", json={"title": "X"}, headers=headers)
    assert response.status_code == 404


def test_update_task_wrong_user(client, created_task, headers2):
    response = client.put(
        f"/tasks/{created_task['id']}",
        json={"title": "Hacked"},
        headers=headers2,
    )
    assert response.status_code == 403


def test_delete_task(client, headers, created_task):
    response = client.delete(f"/tasks/{created_task['id']}", headers=headers)
    assert response.status_code == 200


def test_delete_task_wrong_user(client, created_task, headers2):
    response = client.delete(f"/tasks/{created_task['id']}", headers=headers2)
    assert response.status_code == 403


def test_delete_task_not_found(client, headers):
    response = client.delete("/tasks/99999", headers=headers)
    assert response.status_code == 404
