from enum import Enum

from tortoise import fields, models


class Base(models.Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class CreatedAtMixin:
    created_at = fields.DatetimeField(auto_now_add=True)


class UpdatedAtMixin:
    updated_at = fields.DatetimeField(auto_now=True)


class NameMixin:
    name = fields.CharField(max_length=20, nullable=False)


class ContentMixin:
    content = fields.CharField(max_length=2048, nullable=False)


#######################################################################
# table models.
#######################################################################


class Users(Base, CreatedAtMixin, UpdatedAtMixin):
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=128, unique=True, nullable=False)
    password = fields.CharField(max_length=128, nullable=True)


class Chats(Base, NameMixin, CreatedAtMixin, UpdatedAtMixin):
    user = fields.ForeignKeyField("models.Users", related_name="chats")
    assist_role = fields.CharField(max_length=2048, nullable=True)


class Role(str, Enum):
    System: str = "system"
    User: str = "user"
    Assistant: str = "assistant"


class Messages(Base, ContentMixin, CreatedAtMixin):
    chat = fields.ForeignKeyField("models.Chats", related_name="messages")
    role = fields.CharEnumField(Role, default=Role.User)
