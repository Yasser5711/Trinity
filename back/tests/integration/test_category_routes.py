def test_get_categories(client, sample_category):
    response = client.get("/categories")
    assert response.status_code == 200
    assert any(c["id"] == sample_category.id for c in response.json())


def test_get_categories_top_limit(client):
    from tests.factories.category_factory import CategoryFactory

    for _ in range(5):
        CategoryFactory()
    response = client.get("/categories?top=3")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_category(client, admin_auth_header):
    payload = {"name": "TestCategory"}
    response = client.post("/categories", json=payload, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json()["name"] == "TestCategory"


def test_create_category_duplicate(client, sample_category, admin_auth_header):
    payload = {"name": sample_category.name}
    response = client.post("/categories", json=payload, headers=admin_auth_header)
    assert response.status_code == 400
    assert response.json()["detail"] == "Category already exists"


def test_update_category(client, sample_category, admin_auth_header):
    payload = {"name": "UpdatedCategory"}
    response = client.put(
        f"/categories/{sample_category.id}", json=payload, headers=admin_auth_header
    )
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedCategory"


def test_update_category_not_found(client, admin_auth_header):
    payload = {"name": "Nothing"}
    response = client.put("/categories/9999", json=payload, headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_delete_category(client, sample_category, admin_auth_header):
    response = client.delete(
        f"/categories/{sample_category.id}", headers=admin_auth_header
    )
    assert response.status_code == 204


def test_delete_category_not_found(client, admin_auth_header):
    response = client.delete("/categories/9999", headers=admin_auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"
