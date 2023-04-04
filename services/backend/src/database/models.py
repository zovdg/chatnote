from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Chats(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.ForeignKeyField("models.Users", "id", on_delete=fields.CASCADE)
    # user = fields.ForeignKeyField("models.Users", related_name="chat")
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class RoundTrips(models.Model):
    id = fields.IntField(pk=True)
    chat = fields.ForeignKeyField("models.Chats", related_name="roundtrips")
    seq = fields.IntField()
    ask = fields.CharField(max_length=1024, null=False)
    ask_at = fields.DatetimeField(auto_now_add=True)
    answer = fields.CharField(max_length=4096, null=True)
    answer_at = fields.DatetimeField(auto_now_add=True)
