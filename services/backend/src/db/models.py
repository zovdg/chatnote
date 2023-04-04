from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=128, unique=True, nullable=False)
    password = fields.CharField(max_length=128, nullable=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Chats(models.Model):
    id = fields.IntField(pk=True)
    # user_id = fields.ForeignKeyField("models.Users", "id", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.Users", related_name="chats")
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Conversations(models.Model):
    id = fields.IntField(pk=True)
    # chat_id = fields.ForeignKeyField("models.Chats", "id", on_delete=fields.CASCADE)
    chat = fields.ForeignKeyField("models.Chats", related_name="conversations")
    seq = fields.IntField()
    ask = fields.CharField(max_length=1024, nullable=False)
    ask_at = fields.DatetimeField(auto_now_add=True)
    answer = fields.CharField(max_length=4096, nullable=True)
    answer_at = fields.DatetimeField(auto_now_add=True)


class ConversationTags(models.Model):
    id = fields.IntField(pk=True)
    round_trip_id = fields.ForeignKeyField(
        "models.Conversations", "id", on_delete=fields.CASCADE
    )
    tag_id = fields.ForeignKeyField("models.Tags", "id", on_delete=fields.CASCADE)


class Tags(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField("models.Users", "id", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=20, nullable=False)

    class Meta:
        unique_together = (("user_id", "name"),)
