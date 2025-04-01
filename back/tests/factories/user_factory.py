import factory
from db.models.models import User
from core.helpers import hash_password


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"

    # id = factory.Sequence(lambda n: n + 1)
    first_name = "Test"
    last_name = "User"
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password = factory.LazyFunction(lambda: hash_password("password123"))
