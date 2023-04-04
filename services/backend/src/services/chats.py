from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from ..db.models import Chats
from ..schemas.token import Status
from ..schemas.chats import ChatOutSchema


async def get_chats():
    return await ChatOutSchema.from_queryset(Chats.all())


async def get_chat(chat_id) -> ChatOutSchema:
    return await ChatOutSchema.from_queryset_single(Chats.get(id=chat_id))


async def create_chat(chat, current_user) -> ChatOutSchema:
    chat_dict = chat.dict(exclude_unset=True)
    chat_dict["user_id"] = current_user.id
    chat_obj = await Chats.create(**chat_dict)
    return await ChatOutSchema.from_tortoise_orm(chat_obj)


async def delete_chat(chat_id, current_user) -> Status:
    try:
        db_chat = await ChatOutSchema.from_queryset_single(Chats.get(id=chat_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found")

    if db_chat.author.id == current_user.id:
        deleted_count = await Chats.filter(id=chat_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found")
        return Status(message=f"Deleted chat {chat_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to update")
