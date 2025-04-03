import repositories.category_repository as category_repository
from db.models.models import Category


def test_get_all_categories(db_session, sample_category):
    categories = category_repository.get_all_categories(db_session)
    assert any(c.id == sample_category.id for c in categories)


def test_get_by_id_found(db_session, sample_category):
    cat = category_repository.get_by_id(db_session, sample_category.id)
    assert isinstance(cat, Category)
    assert cat.id == sample_category.id


def test_get_by_id_not_found(db_session):
    assert category_repository.get_by_id(db_session, 9999) is None


def test_get_by_name_found(db_session, sample_category):
    cat = category_repository.get_by_name(db_session, sample_category.name)
    assert cat.id == sample_category.id


def test_get_by_name_not_found(db_session):
    assert category_repository.get_by_name(db_session, "NonExistent") is None


def test_create_category(db_session):
    cat = Category(name="New Category")
    created = category_repository.create(db_session, cat)
    assert created.id is not None
    assert created.name == "New Category"


def test_update_category(db_session, sample_category):
    updated = category_repository.update(db_session, sample_category, "Updated Name")
    assert updated.name == "Updated Name"


def test_delete_category(db_session, sample_category):
    category_repository.delete(db_session, sample_category)
    assert category_repository.get_by_id(db_session, sample_category.id) is None
