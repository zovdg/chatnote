from typing import List
from fastapi import APIRouter, Depends

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from ..db.models import Role
from .. import schemas
from ..auth import get_current_user
from .. import exceptions
from ..services import chats as chat_service

router = APIRouter(tags=['chat'])


@router.get(
    "/chats",
    response_model=List[schemas.UserOut],
    dependencies=[Depends(get_current_user)],
)
async def get_chats(
    current_user: schemas.UserOut = Depends(get_current_user),
):
    return await chat_service.get_chats(current_user.id)


@router.get(
    "/chat/{chat_id}",
    response_model=schemas.UserOut,
    dependencies=[Depends(get_current_user)],
)
async def get_chat(chat_id: str) -> schemas.ChatOut:
    try:
        return await chat_service.get_chat(chat_id)
    except DoesNotExist:
        raise exceptions.not_found(f"Chat {chat_id} does not exist")


@router.post(
    "/chats",
    response_model=schemas.UserOut,
    dependencies=[Depends(get_current_user)],
)
async def create_chat(
    chat: schemas.ChatIn,
    current_user: schemas.UserOut = Depends(get_current_user),
) -> schemas.ChatOut:
    return await chat_service.create_chat(chat, current_user.id)


@router.patch(
    "/chat/{chat_id}",
    dependencies=[Depends(get_current_user)],
    response_model=schemas.ChatOut,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_note(
    chat_id: str,
    chat: schemas.ChatUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),
) -> schemas.ChatOut:
    return await chat_service.update_chat(chat_id, chat, current_user.id)


@router.delete(
    "/chat/{chat_id}",
    response_model=schemas.Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_chat(
    chat_id: str, current_user: schemas.UserOut = Depends(get_current_user)
):
    return await chat_service.delete_chat(chat_id, current_user.id)


@router.post(
    "/chat/{chat_id}/messages",
    response_model=schemas.MessageOut,
    dependencies=[Depends(get_current_user)],
)
async def chat(
    chat_id: str,
    message: schemas.MessageIn,
    current_user: schemas.UserOut = Depends(get_current_user),
) -> schemas.ChatOut:
    # TODO: check chat is belong to current_user or not.
    _ = current_user

    message.role = Role.User
    _prompt = await chat_service.add_chat_message(chat_id, message)

    # do echo now -- TODO: call OpenAI API.

    message.role = Role.Assistant
    completion = await chat_service.add_chat_message(chat_id, message)

    return completion


@router.get(
    "/chat/{chat_id}/messages",
    response_model=List[schemas.MessageOut],
    dependencies=[Depends(get_current_user)],
)
async def add_chat_message(
    chat_id: str,
    current_user: schemas.UserOut = Depends(get_current_user),
) -> schemas.ChatOut:
    # TODO: check chat is belong to current_user or not.
    _ = current_user

    return await chat_service.get_chat_messages(chat_id)
