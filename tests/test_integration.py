def test_full_user_workflow(client):
    """
    Test the complete workflow: register, login, create task, list, update, delete.
    """
    register_response = client.post(
        "/auth/register",
        json={"email": "workflow@example.com", "password": "securepass123"},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": "workflow@example.com", "password": "securepass123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks", json={"title": "Workflow task", "priority": "high"}, headers=headers
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    list_response = client.get("/tasks", headers=headers)
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    update_response = client.patch(
        f"/tasks/{task_id}", json={"status": "completed"}, headers=headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "completed"

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    final_list_response = client.get("/tasks", headers=headers)
    assert final_list_response.status_code == 200
    assert final_list_response.json()["total"] == 0


def test_pagination_workflow_across_multiple_pages(client):
    """
    Test paginating through multiple pages of tasks using limit and offset.
    """
    client.post(
        "/auth/register",
        json={"email": "pageuser@example.com", "password": "securepass123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "pageuser@example.com", "password": "securepass123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for i in range(7):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=headers)

    page1 = client.get("/tasks?limit=3&offset=0", headers=headers)
    assert page1.status_code == 200
    assert len(page1.json()["items"]) == 3

    page2 = client.get("/tasks?limit=3&offset=3", headers=headers)
    assert page2.status_code == 200
    assert len(page2.json()["items"]) == 3

    page3 = client.get("/tasks?limit=3&offset=6", headers=headers)
    assert page3.status_code == 200
    assert len(page3.json()["items"]) == 1

    page1_ids = {item["id"] for item in page1.json()["items"]}
    page2_ids = {item["id"] for item in page2.json()["items"]}
    page3_ids = {item["id"] for item in page3.json()["items"]}
    assert page1_ids.isdisjoint(page2_ids)
    assert page2_ids.isdisjoint(page3_ids)


def test_combined_filtering_workflow(client):
    """
    Test combining status and priority filters together.
    """
    client.post(
        "/auth/register",
        json={"email": "filteruser@example.com", "password": "securepass123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "filteruser@example.com", "password": "securepass123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/tasks",
        json={"title": "Match", "status": "pending", "priority": "high"},
        headers=headers,
    )
    client.post(
        "/tasks",
        json={"title": "Wrong status", "status": "completed", "priority": "high"},
        headers=headers,
    )
    client.post(
        "/tasks",
        json={"title": "Wrong priority", "status": "pending", "priority": "low"},
        headers=headers,
    )

    response = client.get("/tasks?status=pending&priority=high", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Match"


def test_expired_or_invalid_token_rejected(client):
    """
    Test that an invalid token is rejected across protected endpoints.
    """
    headers = {"Authorization": "Bearer invalid.token.here"}

    response = client.get("/tasks", headers=headers)

    assert response.status_code == 401


def test_sorting_workflow(client):
    """
    Test that sorting by title in ascending order returns tasks in the correct order.
    """
    client.post(
        "/auth/register",
        json={"email": "sortuser@example.com", "password": "securepass123"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "sortuser@example.com", "password": "securepass123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/tasks", json={"title": "Zebra"}, headers=headers)
    client.post("/tasks", json={"title": "Apple"}, headers=headers)
    client.post("/tasks", json={"title": "Mango"}, headers=headers)

    response = client.get("/tasks?sort_by=title&sort_order=asc", headers=headers)

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == ["Apple", "Mango", "Zebra"]
