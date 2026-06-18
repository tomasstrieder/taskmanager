def test_get_metrics_no_auth(client):
    response = client.get("/metrics")
    assert response.status_code == 401


def test_get_metrics_empty(client, headers):
    response = client.get("/metrics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 0
    assert data["completed_tasks"] == 0
    assert data["pending_tasks"] == 0
    assert data["in_progress_tasks"] == 0
    assert data["tasks_per_user"] == {}
    assert data["average_completion_time_days"] is None


def test_get_metrics_with_tasks(client, headers, user_payload):
    client.post("/tasks", json={"title": "Task A", "status": "todo"},        headers=headers)
    client.post("/tasks", json={"title": "Task B", "status": "in_progress"}, headers=headers)
    client.post("/tasks", json={"title": "Task C", "status": "done"},        headers=headers)

    response = client.get("/metrics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 3
    assert data["pending_tasks"] == 1
    assert data["in_progress_tasks"] == 1
    assert data["completed_tasks"] == 1
    assert data["average_completion_time_days"] is not None
    assert user_payload["name"] in data["tasks_per_user"]
    assert data["tasks_per_user"][user_payload["name"]] == 3


def test_metrics_response_shape(client, headers):
    response = client.get("/metrics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    expected_keys = {
        "total_tasks",
        "completed_tasks",
        "pending_tasks",
        "in_progress_tasks",
        "tasks_per_user",
        "average_completion_time_days",
    }
    assert expected_keys == set(data.keys())
