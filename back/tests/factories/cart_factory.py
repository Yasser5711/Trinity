import factory
from db.models.models import Cart, CartStatus
from tests.factories.user_factory import UserFactory


class CartFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Cart
        sqlalchemy_session = None
        # sqlalchemy_session_persistence = "flush" temp

        sqlalchemy_session_persistence = "flush"

    user = factory.SubFactory(UserFactory)
    status = CartStatus.PENDING
