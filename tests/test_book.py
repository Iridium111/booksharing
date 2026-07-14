def test_get_books(client):
    response = client.get("/api/v1/books")

    assert response.status_code == 200

def test_filter_books_by_author(client):
    """Тест поиска книг по фильтру."""
    response = client.get("/api/v1/books",
                          params={"author": "Orwell",})

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_book(client):
    """Тест создания книги."""
    create_user_response = client.post("/api/v1/auth/register",
               json={
                   "username": "user_test",
                   "email": "test@mail.ru",
                   "password": "test",
               })

    assert create_user_response.status_code == 201

    login_user_response = client.post("api/v1/auth/login",
                                      json={
                                          "username": "user_test",
                                          "password": "test"
                                      })
    access_token = login_user_response.json()['access_token']

    assert login_user_response.status_code == 200

    response = client.post("/api/v1/books",
                           json={
                               "author": "test",
                               "title": "test",
                               "genre": "test",
                           },
                           headers={"Authorization": f'Bearer {access_token}'})
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "test"
    assert data["author"] == "test"
    assert data["genre"] == "test"

def test_create_book_without_auth(client):
    """Тест создания книги без авторизации."""
    response = client.post("/api/v1/books",
                           json={"author": "test",
                            "title": "test",
                            "genre": "test",})

    assert response.status_code == 401