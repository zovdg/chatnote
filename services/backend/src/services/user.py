from typing import Optional

from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from ..db import models
from .. import schemas
from .. import exceptions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """User Service."""

    @staticmethod
    async def user_create(user: schemas.UserInSchema) -> schemas.UserOutSchema:
        user.password = pwd_context.encrypt(user.password)

        try:
            user_obj = await models.Users.create(**user.dict(exclude_unset=True))
        except IntegrityError:
            raise exceptions.unauthorized(f"Sorry, that username already exists.")

        return await schemas.UserOutSchema.from_tortoise_orm(user_obj)

    @staticmethod
    async def user_delete(
        user_id, current_user_id: Optional[str] = None
    ) -> schemas.Status:
        try:
            db_user = await schemas.UserOutSchema.from_queryset_single(
                models.Users.get(id=user_id)
            )
        except DoesNotExist:
            raise exceptions.not_found(f"User {user_id} not found")

        if current_user_id and db_user.id == current_user_id:
            delete_count = await models.Users.filter(id=user_id).delete()
            if not delete_count:
                raise exceptions.not_found(f"User {user_id} not found")
            return schemas.Status(message=f"Deleted user {user_id}")

        raise exceptions.forbidden(f"Not authorized to delete User {user_id}")
