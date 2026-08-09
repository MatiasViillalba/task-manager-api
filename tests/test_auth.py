def test_register_user_success(client):
    """
    Test that a new user can register successfully with valid data.
    """
    response = client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "securepass123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_user_duplicate_email(client):
    """
    Test that registering with an already used email fails.
    """
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "securepass123"},
    )

    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpass456"},
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_register_user_invalid_email(client):
    """
    Test that registering with an invalid email format fails validation.
    """
    response = client.post(
        "/auth/register", json={"email": "not-an-email", "password": "securepass123"}
    )

    assert response.status_code == 422


def test_register_user_short_password(client):
    """
    Test that registering with a password shorter than 8 characters fails.
    """
    response = client.post(
        "/auth/register", json={"email": "shortpass@example.com", "password": "123"}
    )

    assert response.status_code == 422


def test_login_success(client):
    """
    Test that a registered user can log in and receive a valid JWT token.
    """
    client.post(
        "/auth/register",
        json={"email": "logintest@example.com", "password": "securepass123"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "logintest@example.com", "password": "securepass123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """
    Test that logging in with an incorrect password fails.
    """
    client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": "correctpass123"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "wrongpass@example.com", "password": "incorrectpass456"},
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """
    Test that logging in with an email that was never registered fails.
    """
    response = client.post(
        "/auth/login",
        json={"email": "doesnotexist@example.com", "password": "somepassword123"},
    )

    assert response.status_code == 401
