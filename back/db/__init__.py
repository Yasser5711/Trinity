from .models.models import Base, SessionLocal, User, engine
from .schemas.auth_schemas import UserCreate, UserLogin
from .schemas.schemas import Token


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
