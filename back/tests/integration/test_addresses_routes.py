def test_get_addresses(client, auth_header):
    response = client.get("/client/addresses", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_address(client, auth_header):
    payload = {
        "address_line": "999 New St",
        "city": "CityName",
        "country": "Country",
        "zip_code": "12345",
    }
    response = client.post("/client/addresses", json=payload, headers=auth_header)
    assert response.status_code == 201
    assert response.json()["address_line"] == "999 New St"


def test_update_address(client, auth_header, sample_address):
    payload = {
        "address_line": "Updated Address",
        "city": "Updated City",
        "country": "Updated Country",
        "zip_code": "00000",
    }
    response = client.put(
        f"/client/addresses/{sample_address.id}", json=payload, headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["city"] == "Updated City"


def test_delete_address(client, auth_header, sample_address):
    response = client.delete(
        f"/client/addresses/{sample_address.id}", headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Address deleted successfully"
