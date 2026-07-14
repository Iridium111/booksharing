
def test_user_create(client):
    response = client.post("/api/v1/users/",
                           json={
                               "username": "test",
                               "email": "test@mail.ru",
                               "password": "test",
                           })
    data = response.json()

    assert response.status_code == 201
    assert data["username"] == "test"
    assert data["email"] == "test@mail.ru"
    assert "password" not in data

def test_create_user_with_duplicate_email(client):
    """Тест на создание user с одинаковыми email."""
    first_response = client.post("/api/v1/auth/register",
                           json={
                               "username": "test_user_create",
                               "email": "create@mail.ru",
                               "password": "test",
                           })
    second_response = client.post("/api/v1/auth/register",
                                  json={
                                      "username": "test_user_create1",
                                      "email": "create@mail.ru",
                                      "password": "test1",
                                  })

    assert first_response.status_code == 201
    assert second_response.status_code == 400
