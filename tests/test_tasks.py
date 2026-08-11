def register_and_login(client, email="taskuser@example.com", password="securepass123"):
    """
    Register a new user and log in, returning the authorization headers.

    Args:
        client: The test client fixture.
        email: Email to register the user with.
        password: Password to register the user with.

    Returns:
        A dictionary with the Authorization header set to the user's JWT token.
    """
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_task_success(client):
    """
    Test that an authenticated user can create a task successfully.
    """
    headers = register_and_login(client)

    response = client.post(
        "/tasks", json={"title": "Test task", "priority": "high"}, headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"


def test_create_task_without_auth(client):
    """
    Test that creating a task without authentication fails.
    """
    response = client.post("/tasks", json={"title": "Test task"})

    assert response.status_code == 401


def test_get_tasks_returns_only_own_tasks(client):
    """
    Test that a user only sees their own tasks, not tasks from other users.
    """
    headers_user1 = register_and_login(client, "user1@example.com", "securepass123")
    headers_user2 = register_and_login(client, "user2@example.com", "securepass123")

    client.post("/tasks", json={"title": "User1 task"}, headers=headers_user1)
    client.post("/tasks", json={"title": "User2 task"}, headers=headers_user2)

    response = client.get("/tasks", headers=headers_user1)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "User1 task"


def test_get_single_task_success(client):
    """
    Test that a user can retrieve a single task they own.
    """
    headers = register_and_login(client)

    create_response = client.post(
        "/tasks", json={"title": "Single task"}, headers=headers
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Single task"


def test_get_single_task_not_found(client):
    """
    Test that retrieving a nonexistent task returns 404.
    """
    headers = register_and_login(client)

    response = client.get("/tasks/9999", headers=headers)

    assert response.status_code == 404


def test_get_task_belonging_to_another_user(client):
    """
    Test that a user cannot retrieve a task belonging to another user.
    """
    headers_user1 = register_and_login(client, "owner@example.com", "securepass123")
    headers_user2 = register_and_login(client, "intruder@example.com", "securepass123")

    create_response = client.post(
        "/tasks", json={"title": "Private task"}, headers=headers_user1
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers_user2)

    assert response.status_code == 404


def test_update_task_success(client):
    """
    Test that a user can update a task they own.
    """
    headers = register_and_login(client)

    create_response = client.post(
        "/tasks", json={"title": "Original title"}, headers=headers
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}", json={"status": "completed"}, headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["title"] == "Original title"


def test_update_task_belonging_to_another_user(client):
    """
    Test that a user cannot update a task belonging to another user.
    """
    headers_user1 = register_and_login(client, "owner2@example.com", "securepass123")
    headers_user2 = register_and_login(client, "intruder2@example.com", "securepass123")

    create_response = client.post(
        "/tasks", json={"title": "Protected task"}, headers=headers_user1
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}", json={"status": "completed"}, headers=headers_user2
    )

    assert response.status_code == 404


def test_delete_task_success(client):
    """
    Test that a user can delete a task they own.
    """
    headers = register_and_login(client)

    create_response = client.post(
        "/tasks", json={"title": "To be deleted"}, headers=headers
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404


def test_delete_task_belonging_to_another_user(client):
    """
    Test that a user cannot delete a task belonging to another user.
    """
    headers_user1 = register_and_login(client, "owner3@example.com", "securepass123")
    headers_user2 = register_and_login(client, "intruder3@example.com", "securepass123")

    create_response = client.post(
        "/tasks", json={"title": "Untouchable task"}, headers=headers_user1
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers_user2)

    assert response.status_code == 404


def test_pagination_limits_results(client):
    """
    Test that pagination correctly limits the number of returned tasks.
    """
    headers = register_and_login(client)

    for i in range(5):
        client.post("/tasks", json={"title": f"Task {i}"}, headers=headers)

    response = client.get("/tasks?limit=2&offset=0", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2


def test_filter_by_status(client):
    """
    Test that filtering by status returns only matching tasks.
    """
    headers = register_and_login(client)

    client.post(
        "/tasks", json={"title": "Pending task", "status": "pending"}, headers=headers
    )
    client.post(
        "/tasks",
        json={"title": "Completed task", "status": "completed"},
        headers=headers,
    )

    response = client.get("/tasks?status=completed", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Completed task"


def test_filter_by_priority(client):
    """
    Test that filtering by priority returns only matching tasks.
    """
    headers = register_and_login(client)

    client.post(
        "/tasks", json={"title": "Low priority", "priority": "low"}, headers=headers
    )
    client.post(
        "/tasks", json={"title": "High priority", "priority": "high"}, headers=headers
    )

    response = client.get("/tasks?priority=high", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "High priority"


def test_create_task_with_empty_title_fails(client):
    """
    Test that creating a task with an empty title fails validation.
    """
    headers = register_and_login(client, "emptytitle@example.com", "securepass123")

    response = client.post("/tasks", json={"title": ""}, headers=headers)

    assert response.status_code == 422


def test_create_task_with_title_too_long_fails(client):
    """
    Test that creating a task with a title over 255 characters fails validation.
    """
    headers = register_and_login(client, "longtitle@example.com", "securepass123")

    response = client.post("/tasks", json={"title": "a" * 256}, headers=headers)

    assert response.status_code == 422


def test_update_nonexistent_task_returns_404(client):
    """
    Test that updating a task that doesn't exist returns 404.
    """
    headers = register_and_login(client, "updatenone@example.com", "securepass123")

    response = client.patch(
        "/tasks/99999", json={"status": "completed"}, headers=headers
    )

    assert response.status_code == 404


def test_delete_nonexistent_task_returns_404(client):
    """
    Test that deleting a task that doesn't exist returns 404.
    """
    headers = register_and_login(client, "deletenone@example.com", "securepass123")

    response = client.delete("/tasks/99999", headers=headers)

    assert response.status_code == 404
