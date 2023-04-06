from pydantic import BaseModel
from typing import List

from tortoise.contrib.pydantic import pydantic_model_creator

from ..db.models import Conversations
from .tags import TagOutSchema

ConversationInSchema = pydantic_model_creator(
    Conversations,
    name="ConversationIn",
    exclude=("id", "chat_id"),
    exclude_readonly=True,
)
ConversationOutSchema = pydantic_model_creator(
    Conversations,
    name="ConversationOut",
)


class ConversationOutSchemaList(BaseModel):
    conversations: List[ConversationOutSchema]


class Conversation:
    conversation: ConversationOutSchema
    tags: List[TagOutSchema]
