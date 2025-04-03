import pytest

import services.category_service as category_service
from db.schemas.category_schemas import CategoryCreate, CategoryUpdate


def test_get_categories(db_session, sample_category):
    categories = category_service.get_categories(db_session)
    assert any(cat["id"] == sample_category.id for cat in categories)


def test_get_categories_top_limit(db_session):
    from tests.factories.category_factory import CategoryFactory

    for _ in range(5):
        CategoryFactory()

    result = category_service.get_categories(db_session, top=3)
    assert isinstance(result, list)
    assert len(result) == 3


def test_create_category_success(db_session):
    data = CategoryCreate(name="Unique Category")
    new_cat = category_service.create_category(db_session, data)

    assert new_cat.id is not None
    assert new_cat.name == "Unique Category"


def test_create_category_duplicate(db_session, sample_category):
    data = CategoryCreate(name=sample_category.name)
    with pytest.raises(ValueError, match="Category already exists"):
        category_service.create_category(db_session, data)


def test_update_category_success(db_session, sample_category):
    data = CategoryUpdate(name="Updated Category")
    updated = category_service.update_category(db_session, sample_category.id, data)
    assert updated.name == "Updated Category"


def test_update_category_not_found(db_session):
    data = CategoryUpdate(name="Something")
    with pytest.raises(ValueError, match="Category not found"):
        category_service.update_category(db_session, 9999, data)


def test_delete_category_success(db_session, sample_category):
    category_service.delete_category(db_session, sample_category.id)
    with pytest.raises(ValueError, match="Category not found"):
        category_service.delete_category(db_session, sample_category.id)


def test_delete_category_not_found(db_session):
    with pytest.raises(ValueError, match="Category not found"):
        category_service.delete_category(db_session, 9999)
