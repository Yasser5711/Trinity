import services.address_service as address_service
from db.schemas.address_schemas import AddressCreate, AddressUpdate


def test_list_user_addresses(db_session, sample_address):
    addresses = address_service.list_user_addresses(db_session, sample_address.user_id)
    assert len(addresses) >= 1


def test_get_address_by_id(db_session, sample_address):
    found = address_service.get_address_by_id(
        db_session, sample_address.id, sample_address.user_id
    )
    assert found.id == sample_address.id


def test_create_address(db_session, sample_user):
    data = AddressCreate(
        address_line="456 Side St",
        city="NewCity",
        country="NewCountry",
        zip_code="67890",
    )
    created = address_service.create_address(
        db_session, sample_user.id, address_data=data
    )
    assert created.address_line == "456 Side St"


def test_update_address(db_session, sample_address):
    update_data = AddressUpdate(city="UpdatedCity")
    updated = address_service.update_address(db_session, sample_address, update_data)
    assert updated.city == "UpdatedCity"


def test_delete_address(db_session, sample_address):
    address_service.delete_address(db_session, sample_address)
    result = address_service.get_address_by_id(
        db_session, sample_address.id, sample_address.user_id
    )
    assert result is None
