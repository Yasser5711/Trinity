def test_get_kpis(client, admin_auth_header):
    response = client.get("/kpis", headers=admin_auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_kpi(client, admin_auth_header):
    payload = {
        "name": "Revenue Growth",
        "value": 12.5
    }
    response = client.post("/kpis", json=payload, headers=admin_auth_header)
    assert response.status_code == 201
    assert response.json()["name"] == "Revenue Growth"
    assert response.json()["value"] == 12.5


def test_get_kpi_by_id(client, admin_auth_header):
    # First, create a KPI
    payload = {"name": "User Retention", "value": 87.3}
    kpi = client.post("/kpis", json=payload, headers=admin_auth_header).json()

    response = client.get(f"/kpis/{kpi['id']}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == kpi["id"]
    assert response.json()["name"] == "User Retention"


def test_update_kpi(client, admin_auth_header):
    payload = {"name": "Conversion Rate", "value": 4.0}
    kpi = client.post("/kpis", json=payload, headers=admin_auth_header).json()

    update_payload = {"value": 5.5}
    response = client.put(
        f"/kpis/{kpi['id']}", json=update_payload, headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "KPI updated successfully"


def test_delete_kpi(client, admin_auth_header):
    payload = {"name": "Bounce Rate", "value": 32.0}
    kpi = client.post("/kpis", json=payload, headers=admin_auth_header).json()

    response = client.delete(f"/kpis/{kpi['id']}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "KPI deleted successfully"

    not_found = client.get(f"/kpis/{kpi['id']}", headers=admin_auth_header)
    assert not_found.status_code == 404
