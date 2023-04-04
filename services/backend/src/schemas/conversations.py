from tortoise.contrib.pydantic import pydantic_model_creator

from ..db.models import Conversations

ConversationInSchema = pydantic_model_creator(
    Conversations, name="ConversationIn", exclude=("id",), exclude_readonly=True
)
ConversationOutSchema = pydantic_model_creator(
    Conversations,
    name="Conversation",
)
