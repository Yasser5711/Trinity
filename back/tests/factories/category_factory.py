import factory

from db.models.models import Category


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    name = factory.Sequence(lambda n: f"Category {n}")
