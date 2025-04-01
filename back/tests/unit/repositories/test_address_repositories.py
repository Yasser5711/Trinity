import repositories.address_repository as address_repository
from db.schemas.address_schemas import AddressCreate, AddressUpdate


def test_get_user_addresses(db_session, sample_address):
    addresses = address_repository.get_user_addresses(
        db_session, sample_address.user_id)
    assert len(addresses) >= 1
    assert addresses[0].id == sample_address.id


def test_get_by_id(db_session, sample_address):
    result = address_repository.get_by_id(
        db_session, sample_address.id, sample_address.user_id)
    assert result.id == sample_address.id


def test_create_address(db_session, sample_user):
    payload = AddressCreate(
        address_line="123 Main St",
        city="Anytown",
        country="USA",
        zip_code="12345"
    )
    created = address_repository.create(
        db_session, sample_user.id, address_data=payload)
    assert created.id
    assert created.address_line == "123 Main St"


def test_update_address(db_session, sample_address):
    update_data = AddressUpdate(city="New City")
    updated = address_repository.update(
        db_session, sample_address, update_data=update_data)

    assert updated.city == "New City"


def test_delete_address(db_session, sample_address):
    address_repository.delete(db_session, sample_address)
    result = address_repository.get_by_id(
        db_session, sample_address.id, sample_address.user_id)
    assert result is None
