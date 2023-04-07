from typing import Optional, List

from tortoise.exceptions import DoesNotExist

from ..db import models
from .. import exceptions
from .. import schemas


async def get_chats(user_id: Optional[str] = None):
    model = models.Chats
    if user_id:
        model = model.filter(user_id=user_id)
    return await schemas.ChatOut.from_queryset(model.all())


async def get_chat(chat_id: str) -> schemas.ChatOut:
    return await schemas.ChatOut.from_queryset_single(models.Chats.get(id=chat_id))


async def create_chat(chat: schemas.ChatIn, user_id) -> schemas.ChatOut:
    chat_dict = chat.dict(exclude_unset=True)
    chat_dict["user_id"] = user_id
    chat_obj = await models.Chats.create(**chat_dict)
    return await schemas.ChatOut.from_tortoise_orm(chat_obj)


async def update_chat(
    chat_id: str, chat: schemas.ChatUpdate, current_user_id: str
) -> schemas.ChatOut:
    try:
        db_chat = await schemas.ChatOut.from_queryset_single(
            models.Chats.get(id=chat_id)
        )
    except DoesNotExist:
        raise exceptions.not_found(f"Chat {chat_id} not found")

    if db_chat.user_id == current_user_id:
        await models.Chats.filter(id=chat_id).update(**chat.dict(exclude_unset=True))
        return await schemas.ChatOut.from_queryset_single(models.Chats.get(id=chat_id))

    raise exceptions.forbidden(f"Not authorized to update Chat {chat_id}")


async def delete_chat(chat_id: str, current_user_id: str) -> schemas.Status:
    try:
        db_chat = await schemas.ChatOut.from_queryset_single(
            models.Chats.get(id=chat_id)
        )
    except DoesNotExist:
        raise exceptions.not_found(f"Chat {chat_id} not found")

    if db_chat.user.id == current_user_id:
        deleted_count = await models.Chats.filter(id=chat_id).delete()
        if not deleted_count:
            raise exceptions.not_found(f"Chat {chat_id} not found")
        return schemas.Status(message=f"Deleted chat {chat_id}")

    raise exceptions.forbidden(f"Not authorized to delete Chat {chat_id}")


async def add_chat_message(
    chat_id: str, message: schemas.MessageIn
) -> schemas.MessageOut:
    message_dict = message.dict(exclude_unset=True)
    message_dict["chat_id"] = chat_id
    message_obj = await models.Messages.create(**message_dict)
    return await schemas.MessageOut.from_tortoise_orm(message_obj)


async def get_chat_messages(chat_id: str) -> List[schemas.MessageOut]:
    try:
        db_chat = await schemas.ChatOut.from_queryset_single(
            models.Chats.get(id=chat_id)
        )
    except DoesNotExist:
        raise exceptions.not_found(f"Chat {chat_id} not found")

    return await db_chat.messages.all()
