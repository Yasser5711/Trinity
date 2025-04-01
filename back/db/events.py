from sqlalchemy import event
from sqlalchemy.sql import select

from db.models import models


def assign_default_role_after_insert(mapper, connection, target):
    result = connection.execute(
        select(models.Role).where(models.Role.name == "user"))
    user_role = result.fetchone()

    if not user_role:
        raise Exception("Default role not found")

    connection.execute(
        models.UserRole.__table__.insert(),
        {"user_id": target.id, "role_id": user_role.id},
    )


event.listen(models.User, 'after_insert', assign_default_role_after_insert)
