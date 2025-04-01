def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert "products" in response.json()
    assert "total" in response.json()


def test_get_product_by_id(client, sample_product):
    response = client.get(f"/products/{sample_product.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_product.id


def test_get_product_by_barcode(client, sample_product):
    response = client.get(f"/products/barcode/{sample_product.barCode}")
    assert response.status_code == 200
    assert response.json()["barCode"] == sample_product.barCode


def test_create_product(client, admin_auth_header, sample_category):
    payload = {
        "name": "Test Product",
        "barCode": "1234567891234",
        "nutriScore": "A",
        "price": 10.5,
        "description": "Test description",
        "brand": "TestBrand",
        "category_id": sample_category.id,
        "quantity": "1 unit",
        "nutrition": {},
        "ingredients": "water",
        "allergens": ""
    }
    response = client.post("/products", json=payload,
                           headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"


def test_update_product(client, admin_auth_header, sample_product):
    payload = {"price": 19.99}
    response = client.put(
        f"/products/{sample_product.id}", json=payload, headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["price"] == 19.99


def test_delete_product(client, admin_auth_header, sample_product):
    response = client.delete(
        f"/products/{sample_product.id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"


def test_get_top_products(client):
    response = client.get("/top-products?top=3")
    assert response.status_code == 200
    assert "products" in response.json()


def test_product_pagination_first_page(client, sample_product):
    response = client.get("/products?limit=5&page=1")
    data = response.json()

    assert response.status_code == 200
    assert "products" in data
    assert isinstance(data["products"], list)
    assert data["page"] == 1
    assert data["limit"] == 5


def test_product_pagination_out_of_range(client):
    response = client.get("/products?limit=5&page=9999")
    data = response.json()

    assert response.status_code == 200
    assert data["products"] == []
    assert "message" in data
    assert "out of range" in data["message"]


def test_product_filter_by_name(client, sample_product):
    response = client.get(f"/products?name={sample_product.name}")
    data = response.json()

    assert response.status_code == 200
    assert any(sample_product.name in prod["name"]
               for prod in data["products"])


def test_product_filter_by_brand(client, sample_product):
    response = client.get(f"/products?brand={sample_product.brand}")
    data = response.json()

    assert response.status_code == 200
    assert all(prod["brand"] ==
               sample_product.brand for prod in data["products"])


def test_product_filter_by_category(client, sample_product):
    response = client.get(
        f"/products?category_id={sample_product.category_id}")
    data = response.json()

    assert response.status_code == 200
    assert all(prod["category"]["id"] ==
               sample_product.category_id for prod in data["products"] if prod["category"])


def test_product_filter_by_price_range(client):
    response = client.get("/products?price_min=5&price_max=15")
    data = response.json()

    assert response.status_code == 200
    assert all(5 <= prod["price"] <= 15 for prod in data["products"])
