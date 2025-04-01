import factory
from db.models.models import Stock
from tests.factories.product_factory import ProductFactory
from db.session import SessionLocal


class StockFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Stock
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    product = factory.SubFactory(ProductFactory)
    product_id = factory.SelfAttribute("product.id")
    quantity = factory.Faker("random_int", min=1, max=100)
