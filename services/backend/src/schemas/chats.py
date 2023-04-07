from pydantic import BaseModel
from typing import List, Optional

from tortoise.contrib.pydantic import pydantic_model_creator

from ..db import models as db_models


ChatIn = pydantic_model_creator(
    db_models.Chats, name="ChatIn", exclude=("user_id",), exclude_readonly=True
)
ChatOut = pydantic_model_creator(
    db_models.Chats,
    name="ChatOut",
    exclude=("updated_at",),
)

MessageIn = pydantic_model_creator(
    db_models.Messages, name="MessageIn", exclude=("chat_id", "role"), exclude_readonly=True
)
MessageOut = pydantic_model_creator(db_models.Messages, name="MessageOut")


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    assist_role: Optional[str] = None
