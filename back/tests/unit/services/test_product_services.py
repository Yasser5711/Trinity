import services.product_service as product_service
from db.schemas.product_schemas import ProductCreate, ProductUpdate


def test_get_product_by_id_service(db_session, sample_product):
    product = product_service.get_product_by_id(db_session, sample_product.id)
    assert product.id == sample_product.id


def test_get_product_by_barcode_service(db_session, sample_product):
    product = product_service.get_product_by_barcode(db_session, sample_product.barCode)
    assert product.id == sample_product.id


def test_create_product_service(db_session, sample_category):
    data = ProductCreate(
        name="ServiceProduct",
        barCode="1112223334445",
        nutriScore="B",
        price=12.0,
        description="Created via service",
        brand="SBrand",
        category_id=sample_category.id,
        quantity="500g",
        nutrition={},
        ingredients="stuff",
        allergens="",
    )
    created = product_service.create_product(db_session, data)
    assert created.name == "ServiceProduct"


def test_update_product_service(db_session, sample_product):
    updated = product_service.update_product(
        db_session, sample_product.id, ProductUpdate(price=99.9)
    )
    assert updated.price == 99.9


def test_delete_product_service(db_session, sample_product):
    product_service.delete_product(db_session, sample_product.id)
    assert product_service.get_product_by_id(db_session, sample_product.id) is None


def test_get_products_pagination_and_filter(db_session, sample_product):
    filters = {"name": sample_product.name}
    result = product_service.get_products(db_session, filters, limit=10, page=1)
    assert "products" in result
    assert result["total"] >= 1


def test_get_top_random_products_service(db_session):
    top_products = product_service.get_top_random_products(db_session, 5)
    assert isinstance(top_products, list)
