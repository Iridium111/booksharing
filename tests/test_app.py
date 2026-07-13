

def test_swagger_docs_available(client):
    response = client.get("/docs")

    assert response.status_code == 200

def test_get_books(client):
    response = client.get("/api/v1/books")
    print(response.json())

    assert response.status_code == 200

def test_filter_books_by_author(client):
    response = client.get("/api/v1/books",
                          params={"author": "Orwell",})
    print(response.url)
    print(response.json())

    assert response.status_code == 200
    assert isinstance(response.json(), list)