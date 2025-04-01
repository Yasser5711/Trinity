import factory
from db.models.models import Product
from tests.factories.category_factory import CategoryFactory


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("word")
    nutriScore = "A"
    barCode = factory.Faker("ean13")
    picture = None
    price = 10.0
    description = factory.Faker("sentence")
    brand = factory.Faker("company")
    category = factory.SubFactory(CategoryFactory)  # assume you have this
    quantity = "1kg"
    nutrition = {}
    ingredients = "Some stuff"
    allergens = ""
