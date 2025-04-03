import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.models.models import Base, Role
from db.session import get_db
from main import app
from tests.factories import (
    AddressFactory,
    CartFactory,
    CartItemFactory,
    CategoryFactory,
    ProductFactory,
    StockFactory,
    UserFactory,
)

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(
#     os.path.dirname(__file__), "../../..")))

DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()

    UserFactory._meta.sqlalchemy_session = db
    AddressFactory._meta.sqlalchemy_session = db
    CartFactory._meta.sqlalchemy_session = db
    CartItemFactory._meta.sqlalchemy_session = db
    CategoryFactory._meta.sqlalchemy_session = db
    ProductFactory._meta.sqlalchemy_session = db
    StockFactory._meta.sqlalchemy_session = db

    yield db
    db.close()


@pytest.fixture
def client(db_session):  # noqa: F811
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def sample_user(db_session):
    return UserFactory()


@pytest.fixture
def sample_address(db_session, sample_user):
    return AddressFactory(user=sample_user)


@pytest.fixture
def auth_header(client, sample_user):
    response = client.post(
        "/auth/login", json={"email": sample_user.email, "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_cart(sample_user):
    return CartFactory(user=sample_user)


@pytest.fixture
def admin_user(db_session):
    from db.models.models import Role

    user = UserFactory()
    role = Role(name="admin")
    user.roles.append(role)
    db_session.add(role)
    db_session.commit()
    return user


@pytest.fixture
def admin_auth_header(client, admin_user):
    response = client.post(
        "/auth/login", json={"email": admin_user.email, "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_cart_item(db_session, sample_product, sample_cart):
    from db.models.models import Stock

    stock = Stock(product_id=sample_product.id, quantity=10)
    db_session.add(stock)
    db_session.commit()

    return CartItemFactory(cart=sample_cart, product=sample_product, quantity=1)


@pytest.fixture
def sample_category(db_session):
    return CategoryFactory()


@pytest.fixture
def sample_product(db_session, sample_category):
    return ProductFactory(category=sample_category)


@pytest.fixture
def sample_role(db_session):
    role = Role(name="admin")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


@pytest.fixture
def sample_stock(db_session):
    return StockFactory()
