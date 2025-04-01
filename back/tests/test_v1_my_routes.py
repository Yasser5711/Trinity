# from unittest.mock import patch, MagicMock
# import json
# from datetime import datetime
# from decimal import Decimal
# from typing import List
# from uuid import uuid4
# import requests
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from core.helpers import hash_password
# from db.models import models
# from db.models.models import Base
# from db.schemas.auth_schemas import UserCreate, UserLogin
# from db.session import get_db
# from main import app

# # Use in-memory DB
# SQLALCHEMY_DATABASE_URL = "sqlite://"

# # Use a single connection for the entire test session
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# # Keep the same connection alive during the whole session
# connection = engine.connect()
# TestingSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=connection)

# # Override the DB dependency


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# # Apply override
# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# # Create tables once and drop after


# @pytest.fixture(autouse=True, scope="function")
# def setup_and_teardown():
#     Base.metadata.create_all(bind=connection)
#     yield
#     for table in reversed(Base.metadata.sorted_tables):
#         connection.execute(table.delete())
#     connection.commit()
#     Base.metadata.drop_all(bind=connection)


# ##!Helpers
# def setup_admin_user():
#     db = next(override_get_db())
#     hashed_password = hash_password("admin123")
#     admin_role = models.Role(name="admin")
#     admin_user = models.User(
#         first_name="Admin",
#         last_name="User",
#         email="admin@test.com",
#         password=hashed_password,
#     )
#     admin_user.roles.append(admin_role)
#     db.add_all([admin_role, admin_user])
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "admin@test.com", "password": "admin123"}
#     )
#     return response.json()["access_token"]


# def setup_user():
#     db = next(override_get_db())
#     hashed_password = hash_password("user123")
#     user_role = models.Role(name="user")
#     user = models.User(
#         first_name="User",
#         last_name="Test",
#         email="user@test.com",
#         password=hashed_password,
#     )
#     user.roles.append(user_role)
#     db.add_all([user_role, user])
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "user@test.com", "password": "user123"}
#     )
#     return response.json()["access_token"]


# @pytest.fixture
# def setup_user_():
#     db = next(override_get_db())
#     hashed_password = hash_password("user123")
#     user = models.User(
#         first_name="User",
#         last_name="Test",
#         email="test@test.com",
#         password=hashed_password,
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     yield user
#     db.delete(user)
#     db.commit()


# @pytest.fixture()
# def setup_address():
#     db = next(override_get_db())
#     address = models.Address(
#         user_id=1,
#         address_line="123 Main St",
#         city="Anytown",
#         country="USA",
#         zip_code="12345",
#     )
#     db.add(address)
#     db.commit()
#     db.refresh(address)
#     yield address
#     db.delete(address)
#     db.commit()


# @pytest.fixture()
# def setup_category():
#     db = next(override_get_db())
#     category = models.Category(name="Category 1")
#     db.add(category)
#     db.commit()
#     db.refresh(category)
#     yield category
#     db.delete(category)
#     db.commit()


# @pytest.fixture(scope="function")
# def setup_sample_product():
#     db = next(override_get_db())

#     product = models.Product(
#         name="Sample Product",
#         description="This is a sample product",
#         price=10.0,
#         barCode="123456789",
#         nutriScore="A",
#         brand="Sample Brand",
#         category_id=1,
#         ingredients="Sample ingredients",
#         allergens="Sample allergens",
#         nutrition={"calories": 100, "sugar": 10, "fat": 5},
#     )
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     yield product
#     db.delete(product)
#     db.commit()


# def setup_grp_product(nb_product=1) -> List[dict]:
#     products = []
#     for i in range(1, nb_product + 1):
#         products.append({
#             "id": i,
#             "nutriScore": "A" if i % 2 == 0 else "B",
#             "barCode": f"123456789{i}",
#             "picture": f"http://example.com/product_{i}.jpg",
#             "price": Decimal(f"{i * 10.00}"),
#             "name": f"Product {i}",
#             "description": f"Description for product {i}",
#             "brand": f"Brand {i % 3}",
#             "category": f"Category {i % 3}"
#         })
#     return products


# @pytest.fixture
# def sample_kpi():
#     db = next(override_get_db())
#     kpi = models.KPI(name="Total Sales", value=10000.0)
#     db.add(kpi)
#     db.commit()
#     db.refresh(kpi)
#     yield kpi
#     db.delete(kpi)
#     db.commit()


# @pytest.fixture
# def sample_invoice():
#     db = next(override_get_db())
#     invoice = models.Invoice(user_id=1, total_amount=0.0)
#     db.add(invoice)
#     db.commit()
#     db.refresh(invoice)
#     yield invoice
#     db.delete(invoice)
#     db.commit()


# @pytest.fixture
# def setup_invoice_item():
#     db = next(override_get_db())
#     item = models.InvoiceItem(invoice_id=1, product_id=1,
#                               quantity=2, unit_price=50.00)
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     yield item
#     db.delete(item)
#     db.commit()


# @pytest.fixture
# def setup_stock():
#     db = next(override_get_db())
#     stock = models.Stock(product_id=1, quantity=50)
#     db.add(stock)
#     db.commit()
#     db.refresh(stock)
#     yield stock
#     db.delete(stock)
#     db.commit()


# @pytest.fixture
# def setup_cart():
#     db = next(override_get_db())
#     cart = models.Cart(user_id=1, status="PENDING")
#     db.add(cart)
#     db.commit()
#     db.refresh(cart)
#     yield cart
#     db.delete(cart)
#     db.commit()


# @pytest.fixture
# def setup_cart_item():
#     db = next(override_get_db())
#     category = models.Category(name="Category 1")
#     db.add(category)
#     db.commit()
#     db.refresh(category)
#     product = models.Product(name="Product 1", description="Description for product 1",
#                              price=10.0, barCode="123456789", nutriScore="A", brand="Brand 1", category_id=category.id)
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     item = models.CartItem(cart_id=1, product_id=product.id, quantity=2)

#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     yield item
#     db.delete(item)
#     db.commit()
#     db.delete(product)
#     db.commit()


# ##!Tests


# def test_register_user():
#     response = client.post(
#         "/auth/register",
#         json={
#             "first_name": "testuser",
#             "last_name": "testuser",
#             "email": "test@example.com",
#             "password": "testpassword",
#         },
#     )
#     print(response.json())
#     assert response.status_code == 201
#     assert response.json() == {"detail": "User created successfully"}


# def test_register_user_duplicate():
#     client.post(
#         "/auth/register",
#         json={
#             "first_name": "testuser",
#             "last_name": "testuser",
#             "email": "test@example.com",
#             "password": "testpassword",
#         },
#     )
#     response = client.post(
#         "/auth/register",
#         json={
#             "first_name": "testuser",
#             "last_name": "testuser",
#             "email": "test@example.com",
#             "password": "testpassword",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Email already registered"}


# def test_login_user():
#     hashed_password = hash_password("testpassword")
#     db = next(override_get_db())
#     db_user = models.User(
#         first_name="testuser",
#         email="test@example.com",
#         password=hashed_password,
#         last_name="testuser",
#     )
#     db.add(db_user)
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "test@example.com", "password": "testpassword"}
#     )
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert response.json()["token_type"] == "bearer"


# def test_login_user_invalid_credentials():
#     response = client.post(
#         "/auth/login",
#         json={"email": "nonexistent@email.com", "password": "wrongpassword"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid credentials"}


# def test_me():
#     hashed_password = hash_password("testpassword")
#     db = next(override_get_db())
#     db_role = models.Role(name="user")
#     db.add(db_role)
#     db.commit()

#     db_user = models.User(
#         first_name="testuser",
#         email="test@example.com",
#         password=hashed_password,
#         last_name="testuser",
#         roles=[db_role],
#     )
#     db.add(db_user)
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "test@example.com", "password": "testpassword"}
#     )
#     token = response.json()["access_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/auth/me", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["first_name"] == "testuser"
#     assert response.json()["email"] == "test@example.com"
#     assert response.json()["last_name"] == "testuser"
#     assert "password" not in response.json()
#     assert [role["name"] for role in response.json()["roles"]] == ["user"]


# def test_update_me():
#     hashed_password = hash_password("testpassword")
#     db = next(override_get_db())
#     db_role = models.Role(name="user")
#     db.add(db_role)
#     db.commit()

#     db_user = models.User(
#         first_name="testuser",
#         email="test@test.com",
#         password=hashed_password,
#         last_name="testuser",
#         roles=[db_role],
#     )
#     db.add(db_user)
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "test@test.com", "password": "testpassword"}
#     )
#     token = response.json()["access_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.put("/auth/me", headers=headers, json={
#                           "first_name": "testuser", "last_name": "testuser", "email": "test@testupdate.com"})
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["first_name"] == "testuser"
#     assert response.json()["email"] == "test@testupdate.com"
#     assert response.json()["last_name"] == "testuser"
#     assert "password" not in response.json()
#     assert [role["name"] for role in response.json()["roles"]] == ["user"]


# def test_delete_me(setup_user_):
#     user = setup_user_
#     token = client.post(
#         "/auth/login", json={"email": user.email, "password": "user123"}
#     ).json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/auth/me", headers=headers)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Account deleted successfully"}

#     response = client.post(
#         "/auth/login", json={"email": user.email, "password": "user123"}
#     )
#     assert response.status_code == 400


# def test_me_unauthenticated():
#     response = client.get("/auth/me")
#     assert response.status_code == 401


# def test_me_with_roles():
#     hashed_password = hash_password("testpassword")
#     db = next(override_get_db())
#     role = models.Role(name="admin")
#     db_user = models.User(
#         first_name="testuser",
#         email="test@test.com",
#         password=hashed_password,
#         last_name="testuser",
#     )
#     db_user.roles.append(role)
#     db.add(db_user)
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "test@test.com", "password": "testpassword"}
#     )
#     token = response.json()["access_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/auth/me", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["first_name"] == "testuser"
#     assert response.json()["email"] == "test@test.com"
#     assert response.json()["last_name"] == "testuser"
#     assert "password" not in response.json()
#     assert len(response.json()["roles"]) == 1
#     assert response.json()["roles"][0]["name"] == "admin"


# def test_logout_user():
#     hashed_password = hash_password("testpassword")
#     db = next(override_get_db())
#     db_user = models.User(
#         first_name="testuser",
#         email="test@example.com",
#         password=hashed_password,
#         last_name="testuser",
#     )
#     db.add(db_user)
#     db.commit()

#     response = client.post(
#         "/auth/login", json={"email": "test@example.com", "password": "testpassword"}
#     )
#     token = response.json()["access_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.post("/auth/logout", headers=headers)
#     assert response.status_code == 200
#     response = client.get("/auth/me", headers=headers)
#     assert response.status_code == 401


# def test_forgot_password(setup_user_):

#     response = client.post(
#         "/auth/forgot-password",
#         json={"email": "test@test.com"},
#     )
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["message"] == "Token has 1hour"
#     assert isinstance(response.json()["token"], str)

#     response = client.post(
#         "/auth/forgot-password",
#         json={"email": "zefzef@zefzef.coe"},
#     )
#     assert response.status_code == 404


# def test_reset_password(setup_user_):
#     response = client.post(
#         "/auth/reset-password",
#         json={"token": "test_token", "password": "newpassword",
#               "confirm_password": "newpassword"},
#     )
#     assert response.status_code == 400

#     response = client.post(
#         "/auth/forgot-password",
#         json={"email": "test@test.com"},
#     )
#     assert response.status_code == 200
#     assert "token" in response.json()
#     token = response.json()["token"]

#     response = client.post(
#         "/auth/reset-password",
#         json={"token": token, "password": "newpassword",
#               "confirm_password": "newpassword"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {"message": "Password reset successfully"}

#     response = client.post(
#         "/auth/login",
#         json={"email": "test@test.com", "password": "user123"},
#     )
#     assert response.status_code == 400

#     response = client.post(
#         "/auth/login",
#         json={"email": "test@test.com", "password": "newpassword"},
#     )
#     assert response.status_code == 200
#     assert "access_token" and "token_type" in response.json()


# def test_get_roles():
#     db = next(override_get_db())
#     role1 = models.Role(name="admin")
#     role2 = models.Role(name="user")
#     admin = models.User(
#         first_name="Admin",
#         last_name="User",
#         email="test@test.com",
#         password=hash_password("password123"),
#     )
#     admin.roles.append(role1)
#     db.add(admin)
#     db.add_all([role1, role2])
#     db.commit()
#     token = client.post(
#         "/auth/login", json={"email": "test@test.com", "password": "password123"}
#     ).json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/admin/roles", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 2
#     assert data[0]["name"] == "admin"
#     assert data[1]["name"] == "user"


# def test_create_role():
#     admin_token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     response = client.post(
#         "/admin/roles",
#         headers=headers,
#         json={"name": "editor"},
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Role created successfully"
#     assert response.json()["role"]["name"] == "editor"

#     assert (
#         "id" in response.json()["role"] and type(
#             response.json()["role"]["id"]) == int
#     )


# def test_create_duplicate_role():
#     admin_token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     role = models.Role(name="editor")
#     db = next(override_get_db())
#     db.add(role)
#     db.commit()

#     response = client.post(
#         "/admin/roles",
#         headers=headers,
#         json={"name": "editor"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Role already exists"}


# def test_update_role():
#     admin_token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     db = next(override_get_db())
#     role = models.Role(name="viewer")
#     db.add(role)
#     db.commit()
#     db.refresh(role)
#     print(role)
#     response = client.put(
#         f"/admin/roles",
#         headers=headers,
#         json={
#             "id": role.id,
#             "name": "viewer-updated",
#         },
#     )
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["message"] == "Role updated successfully"
#     assert response.json()["role"]["name"] == "viewer-updated"
#     assert response.json()["role"]["id"] == role.id


# def test_delete_role():
#     admin_token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     db = next(override_get_db())
#     role = models.Role(name="temporary")
#     db.add(role)
#     db.commit()

#     response = client.delete(f"/admin/roles/{role.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Role deleted successfully"


# def test_add_role_to_user():
#     admin_token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     db = next(override_get_db())
#     user = models.User(
#         first_name="User",
#         last_name="Test",
#         email="user@test.com",
#         password=hash_password("password123"),
#     )
#     role = models.Role(name="member")
#     db.add_all([user, role])
#     db.commit()

#     response = client.post(
#         "/auth/roles",
#         headers=headers,
#         json={"user_id": str(user.id), "role_id": str(role.id)},
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Role added to user successfully"


# def test_remove_role_from_user():
#     admin_token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {admin_token}"}

#     db = next(override_get_db())
#     user = models.User(
#         first_name="User",
#         last_name="Test",
#         email="user@test.com",
#         password=hash_password("password123"),
#     )
#     role = models.Role(name="member")
#     user.roles.append(role)
#     db.add_all([user, role])
#     db.commit()

#     response = client.request(
#         method="DELETE",
#         url="/auth/roles",
#         headers=headers,
#         json={"user_id": user.id, "role_id": role.id},
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Role removed from user successfully"


# def test_get_user_as_admin():

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.get("/admin/users", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#     assert len(response.json()) == 1
#     assert response.json()[0]["id"] == 1
#     assert response.json()[0]["first_name"] == "Admin"
#     assert response.json()[0]["last_name"] == "User"
#     assert response.json()[0]["email"] == "admin@test.com"
#     assert len(response.json()[0]["roles"]) == 1
#     assert response.json()[0]["roles"][0]["name"] == "admin"


# def test_get_user_as_non_admin():

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.get("/admin/users", headers=headers)
#     assert response.status_code == 403
#     assert response.json() == {
#         "detail": "User does not have the required role"}


# def test_get_users_as_admin():

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.get("/admin/users", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#     assert len(response.json()) == 1
#     assert response.json()[0]["first_name"] == "Admin"
#     assert response.json()[0]["last_name"] == "User"
#     assert response.json()[0]["email"] == "admin@test.com"
#     assert len(response.json()[0]["roles"]) == 1
#     assert response.json()[0]["roles"][0]["name"] == "admin"


# def test_get_users_as_non_admin():

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.get("/admin/users", headers=headers)
#     assert response.status_code == 403
#     assert response.json() == {
#         "detail": "User does not have the required role"}


# def test_create_user_as_admin():

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.post(
#         "/admin/users",
#         headers=headers,
#         json={
#             "first_name": "New",
#             "last_name": "User",
#             "email": "newuser@test.com",
#             "password": "newpassword",
#             "role_id": 1,
#         },
#     )
#     print(response.json())
#     assert response.status_code == 201
#     assert response.json()["message"] == "User created successfully"


# def test_create_user_as_non_admin():

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.post(
#         "/admin/users",
#         headers=headers,
#         json={
#             "first_name": "New",
#             "last_name": "User",
#             "email": "newuser@test.com",
#             "password": "newpassword",
#             "role_id": 1,
#         },
#     )
#     assert response.status_code == 403
#     assert response.json() == {
#         "detail": "User does not have the required role"}


# def test_update_user_as_admin():

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     db = next(override_get_db())
#     user = models.User(
#         first_name="Existing",
#         last_name="User",
#         email="existinguser@test.com",
#         password=hash_password("password123"),
#     )
#     db.add(user)
#     db.commit()

#     response = client.put(
#         f"/admin/users/{user.id}",
#         headers=headers,
#         json={"id": user.id, "first_name": "Updated", "last_name": "User"},
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "User updated successfully"


# def test_update_user_as_non_admin():

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     db = next(override_get_db())
#     user = models.User(
#         first_name="Existing",
#         last_name="User",
#         email="existinguser@test.com",
#         password=hash_password("password123"),
#     )
#     db.add(user)
#     db.commit()

#     response = client.put(
#         f"/admin/users/{user.id}",
#         headers=headers,
#         json={"first_name": "Updated", "last_name": "User"},
#     )
#     print(response.json())
#     assert response.status_code == 403
#     assert response.json() == {
#         "detail": "User does not have the required role"}


# def test_delete_user_as_admin(setup_sample_product):
#     product = setup_sample_product
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     db = next(override_get_db())
#     user = models.User(
#         first_name="Delete",
#         last_name="Me",
#         email="deleteme@test.com",
#         password=hash_password("password123"),
#     )
#     db.add(user)
#     db.commit()
#     cart = models.Cart(user_id=user.id, status="PENDING")
#     db.add(cart)
#     db.commit()
#     db.refresh(cart)
#     cart_item = models.CartItem(
#         cart_id=cart.id, product_id=product.id, quantity=2)
#     db.add(cart_item)
#     db.commit()
#     db.refresh(cart_item)

#     response = client.delete(f"/admin/users/{user.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "User deleted successfully"


# def test_delete_user_as_non_admin():

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     db = next(override_get_db())
#     user = models.User(
#         first_name="Delete",
#         last_name="Me",
#         email="deleteme@test.com",
#         password=hash_password("password123"),
#     )
#     db.add(user)
#     db.commit()

#     response = client.delete(f"/admin/users/{user.id}", headers=headers)
#     assert response.status_code == 403
#     assert response.json() == {
#         "detail": "User does not have the required role"}


# def test_get_products(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/products", headers=headers)
#     print(response.json())

#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert len(response.json()) > 0
#     assert response.json()["products"][0]["id"] == product.id
#     assert response.json()["products"][0]["name"] == product.name
#     assert "stock" in response.json()["products"][0]
#     assert "nutrition" in response.json()["products"][0]
#     assert "allergens" in response.json()["products"][0]
#     assert "ingredients" in response.json()["products"][0]
#     assert response.json()[
#         "products"][0]["stock"]["quantity"] == stock.quantity
#     assert "category_id" in response.json()["products"][0]
#     assert "category" in response.json()["products"][0]
#     assert response.json()["products"][0]["category"]["name"] == category.name
#     assert response.json()["products"][0]["category_id"] == category.id
#     assert response.json()["products"][0]["category"]["id"] == category.id


# def test_get_products_1(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock
#     response = client.get("/products")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert len(response.json()) > 0
#     assert response.json()["products"][0]["id"] == product.id
#     assert response.json()["products"][0]["name"] == product.name
#     assert "stock" in response.json()["products"][0]
#     assert "nutrition" in response.json()["products"][0]
#     assert "allergens" in response.json()["products"][0]
#     assert "ingredients" in response.json()["products"][0]
#     assert response.json()[
#         "products"][0]["stock"]["quantity"] == stock.quantity
#     assert "category_id" in response.json()["products"][0]
#     assert "category" in response.json()["products"][0]
#     assert response.json()["products"][0]["category"]["name"] == category.name
#     assert response.json()["products"][0]["category_id"] == category.id
#     assert response.json()["products"][0]["category"]["id"] == category.id


# def test_get_top_products(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock
#     response = client.get("/top-products")
#     print(response.json())
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert len(response.json()) > 0
#     assert response.json()["products"][0]["id"] == product.id


# def test_get_products_with_filters(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock

#     response = client.get(f"/products?name={product.name}")
#     print(response.json())
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert "products" in response.json()
#     assert len(response.json()["products"]) > 0
#     assert all(item["name"].lower() == product.name.lower()
#                for item in response.json()["products"])

#     if product.brand:
#         response = client.get(f"/products?brand={product.brand}")
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)
#         assert "products" in response.json()
#         assert len(response.json()["products"]) > 0
#         assert all(item["brand"].lower() == product.brand.lower()
#                    for item in response.json()["products"])

#     response = client.get(f"/products?category_id={category.id}")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert "products" in response.json()
#     assert len(response.json()["products"]) > 0
#     assert all(item["category_id"] ==
#                category.id for item in response.json()["products"])

#     price_min = product.price - 1
#     price_max = product.price + 1

#     response = client.get(
#         f"/products?price_min={price_min}&price_max={price_max}")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert "products" in response.json()
#     assert len(response.json()["products"]) > 0
#     assert all(price_min <= item["price"] <=
#                price_max for item in response.json()["products"])

#     response = client.get(f"/products?price_min={product.price + 1000}")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert "products" in response.json()
#     assert len(response.json()["products"]) == 0

#     response = client.get("/products?name=NonExistentProductName")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert "products" in response.json()
#     assert len(response.json()["products"]) == 0

#     response = client.get("/products?limit=5&page=1")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert "products" in response.json()
#     assert "total" in response.json()
#     assert "total_pages" in response.json()
#     assert "page" in response.json()
#     assert "next_page" in response.json()
#     assert "prev_page" in response.json()
#     assert "limit" in response.json()
#     assert response.json()["page"] == 1
#     assert response.json()["limit"] == 5
#     assert response.json()["total_pages"] >= 1

#     response = client.get("/products?limit=5&page=2")
#     print(response.json())
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert response.json()["page"] == 2
#     assert response.json()["limit"] == 5
#     assert response.json()["total_pages"] >= 1

#     response = client.get("/products?limit=5&page=1000")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)
#     assert response.json()["page"] == 1000
#     assert response.json()["products"] == []
#     assert "message" in response.json()

#     response = client.get("/products?limit=0")
#     assert response.status_code == 422

#     response = client.get("/products?limit=-1")
#     assert response.status_code == 422

#     response = client.get("/products?page=0")
#     assert response.status_code == 422

#     response = client.get("/products?page=-1")
#     assert response.status_code == 422


# def test_get_product_by_id(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         f"/products/{product.id}", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["id"] == product.id
#     assert response.json()["name"] == product.name
#     assert "stock" in response.json()
#     assert response.json()["stock"]["quantity"] == stock.quantity
#     assert "category_id" in response.json()
#     assert "category" in response.json()
#     assert response.json()["category"]["name"] == category.name
#     assert response.json()["category_id"] == category.id
#     assert response.json()["category"]["id"] == category.id


# def test_get_product_by_code(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         f"/products/barcode/{product.barCode}", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["id"] == product.id
#     assert response.json()["barCode"] == product.barCode
#     assert response.json()["name"] == product.name
#     assert "stock" in response.json()
#     assert response.json()["stock"]["quantity"] == stock.quantity
#     assert "category_id" in response.json()
#     assert "category" in response.json()
#     assert response.json()["category"]["name"] == category.name
#     assert response.json()["category_id"] == category.id
#     assert response.json()["category"]["id"] == category.id


# def test_get_product_by_id_1(setup_category, setup_sample_product, setup_stock):
#     category = setup_category
#     product = setup_sample_product
#     stock = setup_stock
#     response = client.get(
#         f"/products/{product.id}")
#     assert response.status_code == 200
#     assert response.json()["id"] == product.id
#     assert response.json()["name"] == product.name
#     assert "stock" in response.json()
#     assert response.json()["stock"]["quantity"] == stock.quantity
#     assert "category_id" in response.json()
#     assert "category" in response.json()
#     assert response.json()["category"]["name"] == category.name
#     assert response.json()["category_id"] == category.id
#     assert response.json()["category"]["id"] == category.id


# def test_create_product():

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     category = models.Category(name="Category 1")
#     db = next(override_get_db())
#     db.add(category)
#     db.commit()
#     db.refresh(category)

#     payload = {
#         "name": "New Product",
#         "description": "Description for new product",
#         "price": 20.0,
#         "barCode": "987654321",
#         "nutriScore": "B",
#         "category_id": category.id,
#         "brand": "Brand 1",
#     }
#     response = client.post("/products", json=payload, headers=headers)
#     assert response.status_code == 201
#     assert response.json()["name"] == payload["name"]
#     assert response.json()["description"] == payload["description"]
#     assert response.json()["price"] == payload["price"]
#     assert response.json()["barCode"] == payload["barCode"]
#     assert response.json()["nutriScore"] == payload["nutriScore"]


# def test_update_product(setup_sample_product):
#     product = setup_sample_product
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"name": "Updated Product Name", "price": 15.0}
#     response = client.put(
#         f"/products/{product.id}", json=payload, headers=headers
#     )
#     assert response.status_code == 200
#     assert response.json()["name"] == payload["name"]
#     assert response.json()["price"] == payload["price"]


# def test_delete_product(setup_sample_product):
#     product = setup_sample_product
#     stock = models.Stock(product_id=product.id, quantity=50)
#     db = next(override_get_db())
#     db.add(stock)
#     db.commit()
#     db.refresh(stock)

#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(
#         f"/products/{product.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Product deleted successfully"}

#     response = client.get(f"/stocks/{stock.id}", headers=headers)
#     assert response.status_code == 404


# def test_get_kpis(sample_kpi):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/kpis", headers=headers)
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#     assert response.json()[0]["name"] == "Total Sales"


# def test_get_kpi_by_id(sample_kpi):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(f"/kpis/{sample_kpi.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["name"] == sample_kpi.name


# def test_create_kpi():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"name": "New KPI", "value": 500.0}
#     response = client.post("/kpis", json=payload, headers=headers)
#     assert response.status_code == 201


# def test_update_kpi(sample_kpi):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"value": 15000.0}
#     response = client.put(f"/kpis/{sample_kpi.id}",
#                           json=payload, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "KPI updated successfully"


# def test_delete_kpi(sample_kpi):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(f"/kpis/{sample_kpi.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "KPI deleted successfully"


# def test_create_invoice():
#     token = setup_admin_user()
#     products = setup_grp_product(2)

#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.post(
#         "/invoices",
#         json={
#             "user_id": 1,
#             "items": [
#                 {"product_id": products[0]['id'],
#                     "quantity": 1, "price": float(products[0]["price"])},
#                 {"product_id": products[1]['id'],
#                     "quantity": 2, "price": float(products[1]["price"])},
#             ],
#         },
#         headers=headers,
#     )
#     print(response.json())
#     assert response.status_code == 201


# def test_get_total_yearly_sales_invoices():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.get("/invoices/yearly-sales", headers=headers)
#     print(response.json())
#     assert response.status_code == 422

#     response = client.get(
#         "/invoices/yearly-sales", headers=headers, params={"year": 2021})
#     print(response.json())
#     assert response.status_code == 200
#     assert int(response.json()["year"]) == 2021
#     assert "monthly_sales" in response.json()
#     assert "month" and "total" in response.json()["monthly_sales"][0]
#     assert len(response.json()["monthly_sales"]) == 12


# def test_get_total_monthly_sales_invoices():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.get("/invoices/monthly-sales", headers=headers)
#     assert response.status_code == 422

#     response = client.get(
#         "/invoices/monthly-sales", headers=headers, params={"year": 2021, "month": 1}
#     )
#     assert response.status_code == 200
#     assert int(response.json()["year"]) == 2021
#     assert response.json()["month"] == "January"
#     assert "total_sales" in response.json()


# def test_get_invoices():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         "/invoices", headers=headers)
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# def test_get_invoice_by_id(sample_invoice):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         f"/invoices/{sample_invoice.id}", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert "id" in response.json()
#     assert "total_amount" in response.json()
#     assert "user" in response.json()


# def test_update_invoice(sample_invoice):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     products = setup_grp_product(2)
#     response = client.put(
#         f"/invoices/{sample_invoice.id}",
#         json={
#             "items": [
#                 {"product_id": products[0]['id'],
#                     "quantity": 1, "price": float(products[0]["price"])},
#                 {"product_id": products[1]['id'],
#                     "quantity": 2, "price": float(products[1]["price"])},
#             ]
#         },
#         headers=headers,
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Invoice updated successfully"


# def test_delete_invoice(sample_invoice):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.delete(
#         f"/invoices/{sample_invoice.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Invoice deleted successfully"


# def test_get_invoice_items(setup_invoice_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         "/invoice-items", headers=headers)
#     assert response.status_code == 200
#     assert len(response.json()) > 0


# def test_get_invoice_item_by_id(setup_invoice_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(f"/invoice-items/{setup_invoice_item.id}",
#                           headers=headers)
#     assert response.status_code == 200
#     assert response.json()["id"] == 1


# def test_create_invoice_item():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     data = {"invoice_id": 2, "product_id": 3,
#             "quantity": 1, "unit_price": 50.00}
#     response = client.post("/invoice-items", json=data,
#                            headers=headers)
#     assert response.status_code == 201


# def test_update_invoice_item(setup_invoice_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     data = {"quantity": 3}
#     response = client.put(f"/invoice-items/{setup_invoice_item.id}", json=data,
#                           headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Invoice item updated successfully"


# def test_delete_invoice_item(setup_invoice_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(
#         f"/invoice-items/{setup_invoice_item.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Invoice item deleted successfully"


# def test_get_stocks(setup_stock):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         "/stocks", headers=headers)
#     assert response.status_code == 200
#     assert len(response.json()) > 0


# def test_get_stock_by_id(setup_stock):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(
#         f"/stocks/{setup_stock.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["id"] == 1


# def test_create_stock():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     data = {"product_id": 2, "quantity": 30}
#     response = client.post("/stocks", json=data,
#                            headers=headers)
#     assert response.status_code == 201


# def test_update_stock(setup_stock):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     data = {"quantity": 100}
#     response = client.put(f"/stocks/{setup_stock.id}", json=data,
#                           headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Stock updated successfully"


# def test_delete_stock(setup_stock):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(
#         f"/stocks/{setup_stock.id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Stock deleted successfully"


# def test_get_cart_statuses():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/carts/status", headers=headers)
#     assert response.status_code == 200
#     assert "statuses" in response.json()
#     assert "pending" in response.json()["statuses"]
#     assert "completed" in response.json()["statuses"]
#     assert "cancelled" in response.json()["statuses"]


# def test_get_carts():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/carts", headers=headers)
#     assert response.status_code == 200
#     print(response.json())
#     assert type(response.json()) is list
#     assert len(response.json()) >= 0


# def test_create_cart():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"user_id": 1}
#     response = client.post("/carts", json=payload, headers=headers)
#     assert response.status_code == 201


# def test_update_cart():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"status": "completed"}
#     response = client.put("/carts/1", json=payload, headers=headers)
#     assert response.status_code in (200, 400)


# def test_delete_cart():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/carts/1", headers=headers)
#     assert response.status_code in (200, 404)


# def test_get_cart_items():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/cart-items", headers=headers)
#     assert response.status_code == 200
#     print(response.json())
#     assert isinstance(response.json(), list)
#     for item in response.json():
#         assert "id" in item
#         assert "cart_id" in item
#         assert "product_id" in item
#         assert "quantity" in item
#         assert "price" in item


# def test_get_cart_item_by_id(setup_cart_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get(f"/cart-items/{setup_cart_item.id}", headers=headers)
#     if response.status_code == 200:
#         item = response.json()
#         assert "id" in item
#         assert "cart_id" in item
#         assert "product_id" in item
#         assert "quantity" in item
#         assert "price" in item
#     else:
#         print(response.json())
#         assert response.status_code == 404


# def test_create_cart_item(setup_cart_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"cart_id": 1, "product_id": 1, "quantity": 2}
#     response = client.post("/cart-items", json=payload, headers=headers)
#     assert response.status_code == 201
#     response_data = response.json()
#     print(response_data)
#     assert "cart_item_id" in response_data
#     assert "price" in response_data
#     assert response_data["price"] == 20.0


# def test_update_cart_item(setup_cart_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"quantity": 3}
#     response = client.put(
#         f"/cart-items/{setup_cart_item.id}", json=payload, headers=headers)
#     if response.status_code == 200:
#         response_data = response.json()
#         assert "price" in response_data
#         assert response_data["price"] == 30.0
#     else:
#         print(response.json())
#         assert response.status_code == 404


# def test_delete_cart_item(setup_cart_item):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(
#         f"/cart-items/{setup_cart_item.id}", headers=headers)
#     if response.status_code == 200:
#         assert response.json()["message"] == "Cart item deleted successfully"
#     else:
#         print(response.json())
#         assert response.status_code == 404


# def test_create_category():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"name": "Electronics"}
#     response = client.post("/categories", json=payload, headers=headers)
#     assert response.status_code == 201
#     assert response.json()["name"] == "Electronics"
#     assert "id" in response.json()


# def test_get_categories():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/categories", headers=headers)
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# @pytest.mark.parametrize("top_value", range(3, 11))
# def test_get_categories_with_valid_filters(top_value):
#     response = client.get(f"/categories?top={top_value}")
#     print(response.json())
#     assert response.status_code == 200

#     assert len(response.json()) <= top_value
#     assert all(
#         "id" in category and "name" in category and "product_count" in category for category in response.json())


# @pytest.mark.parametrize("top_value", [0, 1, 2])
# def test_get_categories_with_invalid_filters(top_value):
#     response = client.get(f"/categories?top={top_value}")
#     assert response.status_code == 422
#     assert "detail" in response.json()


# def test_update_category(setup_category):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {"name": "Updated Category"}
#     response = client.put(
#         f"/categories/{setup_category.id}", json=payload, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Updated Category"


# def test_delete_category(setup_category):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(
#         f"/categories/{setup_category.id}", headers=headers)
#     assert response.status_code == 204


# def test_get_cart():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/client/cart", headers=headers)
#     assert response.status_code == 200
#     assert "items" in response.json()


# def test_add_cart_item():
#     product = models.Product(
#         name="Product 1",
#         description="Description for product 1",
#         price=10.0,
#         barCode="123456789",
#         nutriScore="A",
#         brand="Brand 1",
#         category_id=1,
#     )
#     db = next(override_get_db())
#     db.add(product)
#     db.commit()

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {
#         "product_id": product.id,
#         "quantity": 2,
#         "cart_id": 1
#     }
#     response = client.post("/client/cart/items", json=payload,
#                            headers=headers)
#     print(response.json())
#     assert response.status_code == 201
#     assert response.json()["quantity"] == payload["quantity"]


# def test_update_cart_item(setup_cart_item, setup_stock):
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {
#         "quantity": 3
#     }

#     response = client.put(
#         f"/client/cart/items/{setup_cart_item.id}", json=payload, headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["quantity"] == payload["quantity"]

#     response = client.get(
#         f"/stocks/{setup_stock.id}", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["quantity"] == 50-payload["quantity"]


# def test_update_cart_item_without_stock(setup_cart_item, setup_stock):
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {
#         "quantity": 300
#     }

#     response = client.put(
#         f"/client/cart/items/{setup_cart_item.id}", json=payload, headers=headers)
#     print(response.json())
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Not enough stock"


# def test_remove_cart_item(setup_cart_item):
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete(
#         f"/client/cart/items/{setup_cart_item.id}", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json() == {"message": "Item removed from cart"}


# def test_checkout(setup_cart):
#     from core.helpers.jwt import verify_token
#     db = next(override_get_db())
#     token = setup_user()
#     user_id = verify_token(f"Bearer {token}", db)
#     headers = {"Authorization": f"Bearer {token}"}

#     db = next(override_get_db())
#     cart = db.query(models.Cart).filter_by(id=setup_cart.id).first()

#     cart.user_id = user_id
#     db.commit()
#     db.refresh(cart)
#     print(cart)

#     product = models.Product(
#         name="Product 1",
#         description="Description for product 1",
#         price=10.0,
#         barCode="123456789",
#         nutriScore="A",
#         brand="Brand 1",
#         category_id=1,
#     )
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     print(product)

#     cart_item = models.CartItem(
#         cart_id=cart.id, product_id=product.id, quantity=2)
#     db.add(cart_item)
#     db.commit()
#     db.refresh(cart_item)
#     print(cart_item)
#     print(cart.items)
#     assert len(cart.items) > 0

#     response = client.post("/client/checkout", headers=headers)

#     print(response.json())
#     assert response.status_code == 201
#     invoice = response.json()

#     assert "id" in invoice
#     assert "total_amount" in invoice
#     assert invoice["total_amount"] > 0
#     assert invoice["user_id"] == int(user_id)

#     db.delete(cart_item)
#     db.delete(product)
#     db.commit()


# def test_get_invoices_client():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/client/invoices", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     invoices = response.json()
#     assert isinstance(invoices, list)
#     if invoices:
#         assert "id" in invoices[0]
#         assert "total_amount" in invoices[0]


# def test_get_my_wishlist():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/client/wishlist", headers=headers)

#     assert response.status_code == 200
#     assert "items" in response.json() and isinstance(
#         response.json()["items"], list)
#     assert "id" in response.json()
#     id_ = response.json()["id"]

#     response = client.get("/client/wishlist", headers=headers)

#     assert response.status_code == 200
#     assert "id" in response.json() and response.json()["id"] == id_


# def test_add_to_wishlist():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     db = next(override_get_db())
#     product = models.Product(
#         name="Product 1",
#         description="Description for product 1",
#         price=10.0,
#         barCode="123456789",
#         nutriScore="A",
#         brand="Brand 1",
#         category_id=1,
#     )
#     db.add(product)
#     db.commit()
#     db.refresh(product)

#     response = client.post(
#         "/client/wishlist/items",
#         json={"product_id": product.id},
#         headers=headers,
#     )

#     assert response.status_code == 201
#     assert "items" and "id" in response.json()
#     assert len(response.json()["items"]) == 1
#     assert response.json()["items"][0]["product_id"] == product.id
#     assert response.json()["items"][0]["product"]["id"] == 1

#     response = client.post(
#         "/client/wishlist/items",
#         json={"product_id": 10000},
#         headers=headers,
#     )
#     assert response.status_code == 400

#     response = client.post(
#         "/client/wishlist/items",
#         json={"product_id": product.id},
#         headers=headers,
#     )
#     assert response.status_code == 400


# def test_remove_from_wishlist():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.delete("/client/wishlist/items/1", headers=headers)

#     assert response.status_code == 404
#     assert response.json() == {'detail': 'Wishlist not found'}

#     db = next(override_get_db())
#     product = models.Product(
#         name="Product 1",
#         description="Description for product 1",
#         price=10.0,
#         barCode="123456789",
#         nutriScore="A",
#         brand="Brand 1",
#         category_id=1,
#     )
#     db.add(product)
#     db.commit()
#     db.refresh(product)

#     response = client.post(
#         "/client/wishlist/items",
#         json={"product_id": product.id},
#         headers=headers,
#     )
#     assert response.status_code == 201
#     assert "items" in response.json()
#     assert len(response.json()["items"]) == 1

#     response = client.delete(f"/client/wishlist/items/1000", headers=headers)
#     assert response.status_code == 404
#     assert response.json() == {'detail': 'Product not found'}

#     response = client.delete(
#         f"/client/wishlist/items/{product.id}", headers=headers)

#     assert response.status_code == 200
#     assert response.json() == {"message": "Product removed from wishlist"}


# def test_delete_wishlist():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/client/wishlist", headers=headers)

#     assert response.status_code == 404
#     assert response.json() == {'detail': 'Wishlist not found'}

#     response = client.get("/client/wishlist", headers=headers)

#     assert response.status_code == 200

#     response = client.delete("/client/wishlist", headers=headers)

#     assert response.status_code == 200
#     assert response.json() == {"message": "Wishlist deleted successfully"}


# def test_generate_report_as_admin():
#     token = setup_admin_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/reports", headers=headers)
#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "application/pdf"


# def test_generate_report_as_non_admin():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/reports", headers=headers)
#     assert response.status_code == 403
#     assert response.json() == {
#         "detail": "User does not have the required role"}


# def test_generate_report_as_non_connected():
#     response = client.get("/reports")
#     assert response.status_code == 401
#     assert response.json() == {
#         "detail": "Authorization token is missing"}


# def test_get_address_by_id(setup_address):
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/client/addresses/1", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert "id" in response.json()
#     assert "user_id" in response.json()
#     assert "address_line" in response.json()
#     assert "city" in response.json()
#     assert "country" in response.json()
#     assert "zip_code" in response.json()


# def test_get_addresses(setup_address):
#     address = setup_address
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/client/addresses", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#     assert "id" in response.json()[0]
#     assert "user_id" in response.json()[0]
#     assert "address_line" in response.json()[0]
#     assert "city" in response.json()[0]
#     assert "country" in response.json()[0]
#     assert "zip_code" in response.json()[0]


# def test_create_address():
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {
#         "address_line": "123, Main Street",
#         "city": "New York",
#         "country": "USA",
#         "zip_code": "10001"
#     }

#     response = client.post("/client/addresses", json=payload, headers=headers)
#     print(response.json())
#     assert response.status_code == 201
#     assert response.json()["address_line"] == payload["address_line"]
#     assert response.json()["city"] == payload["city"]
#     assert response.json()["country"] == payload["country"]
#     assert response.json()["zip_code"] == payload["zip_code"]


# def test_update_address(setup_address):
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     payload = {
#         "address_line": "123, Main Street",
#         "city": "New York",
#         "country": "USA",
#         "zip_code": "10001"
#     }
#     response = client.put("/client/addresses/1", json=payload, headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json()["address_line"] == payload["address_line"]
#     assert response.json()["city"] == payload["city"]
#     assert response.json()["country"] == payload["country"]
#     assert response.json()["zip_code"] == payload["zip_code"]
#     assert response.json()["id"] == 1


# def test_delete_address(setup_address):
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/client/addresses/1", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert response.json() == {"message": "Address deleted successfully"}


# @pytest.fixture
# def mock_paypal_token():
#     with patch("api.controllers.paypal.routes.get_paypal_token", return_value="mocked-access-token"):
#         yield


# @pytest.fixture
# def mock_paypal_capture():
#     """Mocks PayPal capture order API response for /capture-paypal-order/{order_id} only."""
#     original_post = requests.post  # Save the original requests.post method

#     def side_effect(url, *args, **kwargs):
#         if "capture" in url:  # Only mock PayPal capture URL
#             mock_response = MagicMock()
#             mock_response.status_code = 201
#             mock_response.json.return_value = {
#                 "id": "PAYPAL_ORDER_ID",
#                 "status": "COMPLETED",
#                 "purchase_units": [{"amount": {"value": "100.00", "currency_code": "USD"}}],
#             }
#             return mock_response
#         elif "api-m.sandbox" in url:
#             mock_response = MagicMock()
#             mock_response.status_code = 201
#             mock_response.json.return_value = {
#                 "id": "PAYPAL_MOCK_ORDER_ID",
#                 "status": "CREATED",
#                 "links": [
#                     {"href": "https://www.paypal.com/checkoutnow?token=PAYPAL_MOCK_ORDER_ID",
#                         "rel": "self", "method": "GET"},
#                     {"href": "https://www.paypal.com/checkoutnow?token=PAYPAL_MOCK_ORDER_ID",
#                         "rel": "approve", "method": "GET"},
#                     {"href": "https://www.paypal.com/checkoutnow?token=PAYPAL_MOCK_ORDER_ID",
#                         "rel": "update", "method": "GET"},
#                     {"href": "https://www.paypal.com/checkoutnow?token=PAYPAL_MOCK_ORDER_ID",
#                         "rel": "capture", "method": "GET"},
#                 ],
#             }
#             return mock_response
#         else:
#             # Use real request for everything else
#             return original_post(url, *args, **kwargs)

#     with patch("requests.post", side_effect=side_effect) as mock_request:
#         yield mock_request


# @pytest.mark.skip(reason="Skipping this test temporarily")
# def test_create_paypal_order(setup_cart, setup_cart_item, mock_paypal_token, mock_paypal_capture):
#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.post("/client/create-paypal-order/", headers=headers)

#     print(response.json())

#     assert response.status_code == 201
#     assert "id" in response.json()
#     assert response.json()["status"] == "CREATED"
#     assert "links" in response.json()
#     assert len(response.json()["links"]) > 0
#     for link in response.json()["links"]:
#         assert "href" in link
#         assert "rel" in link
#         assert "method" in link
#     expected_links = {"self", "approve", "update", "capture"}
#     actual_links = {link["rel"] for link in response.json()["links"]}

#     assert expected_links.issubset(
#         actual_links), f"Missing links: {expected_links - actual_links}"


# @pytest.mark.skip(reason="Skipping this test temporarily")
# def test_capture_paypal_order(setup_cart, setup_cart_item, setup_stock, mock_paypal_token, mock_paypal_capture):

#     token = setup_user()
#     headers = {"Authorization": f"Bearer {token}"}
#     create_response = client.post(
#         "/client/create-paypal-order/", headers=headers)
#     print(create_response.json())
#     assert create_response.status_code == 201
#     order_id = create_response.json()["id"]
#     assert order_id is not None
#     response = client.post(
#         f"/client/capture-paypal-order/{order_id}", headers=headers)
#     print(response.json())
#     assert response.status_code == 200
#     assert "invoice_id" in response.json()
#     assert response.json()[
#         "message"] == "Order successfully captured and processed"
#     assert mock_paypal_capture.called
