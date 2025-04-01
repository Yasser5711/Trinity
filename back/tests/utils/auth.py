from fastapi.testclient import TestClient


def get_auth_header(client: TestClient, email: str, password: str):
    response = client.post(
        "/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
