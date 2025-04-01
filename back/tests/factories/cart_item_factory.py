import factory
from db.models.models import CartItem
from tests.factories.cart_factory import CartFactory
from tests.factories.product_factory import ProductFactory


class CartItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CartItem
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 2
