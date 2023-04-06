from tortoise import fields, models


class Base(models.Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Users(TimestampMixin, Base):
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=128, unique=True, nullable=False)
    password = fields.CharField(max_length=128, nullable=True)


class Chats(TimestampMixin, Base):
    user = fields.ForeignKeyField("models.Users", related_name="chats")
    name = fields.CharField(max_length=255)


class Conversations(Base):
    chat = fields.ForeignKeyField("models.Chats", related_name="conversations")
    tags = fields.ManyToManyField("models.Tags", related_name="conversations")
    sequence = fields.IntField(nullable=False)
    prompt = fields.CharField(max_length=1024, nullable=False)
    prompt_at = fields.DatetimeField(auto_now_add=True)
    completion = fields.CharField(max_length=4096, nullable=True)
    completion_at = fields.DatetimeField(auto_now_add=True)


class Tags(Base):
    user = fields.ForeignKeyField("models.Users", related_name="tags")
    name = fields.CharField(max_length=20, nullable=False)

    class Meta:
        unique_together = (("user_id", "name"),)
