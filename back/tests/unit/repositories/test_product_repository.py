import repositories.product_repository as product_repository
from tests.factories.product_factory import ProductFactory


def test_create_product_repo(db_session):
    product = ProductFactory()
    result = product_repository.create(db_session, product)
    assert result.id


def test_get_product_by_id_repo(db_session, sample_product):
    result = product_repository.get_by_id(db_session, sample_product.id)
    assert result.id == sample_product.id


def test_get_product_by_barcode_repo(db_session, sample_product):
    result = product_repository.get_by_barcode(db_session, sample_product.barCode)
    assert result.id == sample_product.id


def test_get_paginated_products_repo(db_session, sample_product):
    query = product_repository.get_products_query(db_session)
    results = product_repository.get_paginated(query, offset=0, limit=5)
    assert isinstance(results, list)


def test_delete_product_repo(db_session):
    product = ProductFactory()
    db_session.commit()
    product_repository.delete(db_session, product)
    assert product_repository.get_by_id(db_session, product.id) is None


def test_total_count_repo(db_session):
    total = product_repository.total_count(db_session)
    assert isinstance(total, int)
