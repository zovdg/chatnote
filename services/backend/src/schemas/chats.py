from pydantic import BaseModel
from typing import List

from tortoise.contrib.pydantic import pydantic_model_creator

from ..db.models import Chats
from .conversations import ConversationOutSchema


ChatInSchema = pydantic_model_creator(
    Chats, name="ChatIn", exclude=("user_id",), exclude_readonly=True
)
ChatOutSchema = pydantic_model_creator(
    Chats,
    name="ChatOut",
    exclude=("updated_at",),
)


class ChatOutSchemaList(BaseModel):
    chats: List[ChatOutSchema]


class Chat:
    chat: ChatOutSchema
    conversations: List[ConversationOutSchema]
