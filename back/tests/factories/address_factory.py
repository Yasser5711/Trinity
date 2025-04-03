import factory

from db.models.models import Address
from tests.factories.user_factory import UserFactory


class AddressFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Address
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    user = factory.SubFactory(UserFactory)
    address_line = factory.Faker("street_address")
    city = factory.Faker("city")
    country = factory.Faker("country_code")
    zip_code = factory.Faker("postcode")
