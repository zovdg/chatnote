from typing import Optional, List

from tortoise.exceptions import DoesNotExist

from ..db import models
from .. import exceptions
from .. import schemas


class ChatService:
    """Chat Service."""

    @staticmethod
    async def chat_list(user_id: Optional[str] = None):
        model = models.Chats
        if user_id:
            model = model.filter(user_id=user_id)
        return await schemas.ChatOutSchema.from_queryset(model.all())

    @staticmethod
    async def chat_get(chat_id) -> schemas.ChatOutSchema:
        return await schemas.ChatOutSchema.from_queryset_single(
            models.Chats.get(id=chat_id)
        )

    @staticmethod
    async def chat_create(chat, user_id) -> schemas.ChatOutSchema:
        chat_dict = chat.dict(exclude_unset=True)
        chat_dict["user_id"] = user_id
        chat_obj = await models.Chats.create(**chat_dict)
        return await schemas.ChatOutSchema.from_tortoise_orm(chat_obj)

    @staticmethod
    async def chat_delete(chat_id, user_id) -> schemas.Status:
        try:
            db_chat = await schemas.ChatOutSchema.from_queryset_single(
                models.Chats.get(id=chat_id)
            )
        except DoesNotExist:
            raise exceptions.not_found(f"Chat {chat_id} not found")

        if db_chat.user.id == user_id:
            deleted_count = await models.Chats.filter(id=chat_id).delete()
            if not deleted_count:
                raise exceptions.not_found(f"Chat {chat_id} not found")
            return schemas.Status(message=f"Deleted chat {chat_id}")

        raise exceptions.forbidden(f"Not authorized to delete Chat {chat_id}")

    @staticmethod
    async def conversation_list(
        chat_id: Optional[str] = None,
    ) -> List[schemas.ConversationOutSchema]:
        model = models.Conversations
        if chat_id:
            model = model.filter(chat_id=chat_id)
        model = model.order_by("sequence")
        return await schemas.ConversationOutSchema.from_queryset(model.all())

    @staticmethod
    async def conversation_get(conversation_id: str) -> schemas.ConversationOutSchema:
        return await schemas.ConversationOutSchema.from_queryset_single(
            models.Conversations.get(id=conversation_id)
        )

    @staticmethod
    async def conversation_tag_list(conversation_id: str) -> List[schemas.TagOutSchema]:
        return await schemas.TagOutSchema.from_queryset(
            models.Conversations.get(id=conversation_id).tags.all()
        )

    @staticmethod
    async def conversation_create(
        conversation, chat_id
    ) -> schemas.ConversationOutSchema:
        conversation_dict = conversation.dict(exclude_unset=True)
        conversation_dict["chat_id"] = chat_id
        conversation_obj = await models.Conversations.create(**conversation_dict)
        return await schemas.ConversationOutSchema.from_tortoise_orm(conversation_obj)

    @staticmethod
    async def conversation_delete(
        conversation_id, chat_id: Optional[str] = None
    ) -> schemas.Status:
        try:
            db_conversation = await schemas.ConversationOutSchema.from_queryset_single(
                models.Conversations.get(id=conversation_id)
            )
        except DoesNotExist:
            raise exceptions.not_found(f"Conversation {conversation_id} not found")

        if chat_id and db_conversation.chat.id == chat_id:
            deleted_count = await models.Conversations.filter(
                id=conversation_id
            ).delete()
            if not deleted_count:
                raise exceptions.not_found(f"Conversation {conversation_id} not found")

            return schemas.Status(message=f"Deleted conversation {conversation_id}")

        raise exceptions.forbidden(
            f"Not authorized to delete Conversation {conversation_id}"
        )
