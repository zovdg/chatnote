from tortoise.contrib.pydantic import pydantic_model_creator

from ..db.models import Chats

ChatInSchema = pydantic_model_creator(
    Chats, name="ChatIn", exclude=("user_id",), exclude_readonly=True
)
ChatOutSchema = pydantic_model_creator(
    Chats,
    name="Chat",
    exclude=("updated_at",),
)
