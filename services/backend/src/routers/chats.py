from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from .. import schemas
from .. import auth
from .. import exceptions
from .. import services

router = APIRouter()


@router.get(
    "/chats",
    response_model=schemas.ChatOutSchemaList,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_chats(
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
):
    return await services.ChatService.chat_list(current_user.id)


@router.get(
    "/chat/{chat_id}",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_chat(chat_id: str) -> schemas.ChatOutSchema:
    try:
        return await services.ChatService.chat_get(chat_id)
    except DoesNotExist:
        raise exceptions.not_found(f"Chat {chat_id} does not exist")


@router.post(
    "/chats",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def create_chat(
    chat: schemas.ChatInSchema,
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
) -> schemas.ChatOutSchema:
    return await services.ChatService.chat_create(chat, current_user.id)


@router.delete(
    "/chat/{chat_id}",
    response_model=schemas.Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_chat(
    chat_id: str, current_user: schemas.UserOutSchema = Depends(auth.get_current_user)
):
    return await services.ChatService.chat_delete(chat_id, current_user.id)
