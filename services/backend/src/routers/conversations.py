from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from .. import schemas
from .. import services
from .. import auth
from .. import exceptions

router = APIRouter()


@router.get(
    "/conversations",
    response_model=schemas.ConversationOutSchemaList,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_conversations(
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
):
    return await services.ChatService.conversation_list(current_user.id)


@router.get(
    "/conversation/{conversation_id}",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_conversation(conversation_id: str) -> schemas.ConversationOutSchema:
    try:
        return await services.ChatService.conversation_get(conversation_id)
    except DoesNotExist:
        raise exceptions.not_found(f"Conversation {conversation_id} does not exist")


@router.patch(
    "/conversation/{conversation_id}/tag",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def set_conversation_tag(
    conversation_id: str, tag: str
) -> schemas.ConversationOutSchema:
    try:
        return await services.ChatService.conversation_get(conversation_id)
    except DoesNotExist:
        raise exceptions.not_found(f"Conversation {conversation_id} does not exist")


@router.post(
    "/conversations",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def create_conversation(
    conversation: schemas.ConversationInSchema,
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
) -> schemas.ConversationOutSchema:
    return await services.ChatService.conversation_create(conversation, current_user.id)


@router.delete(
    "/conversation/{conversation_id}",
    response_model=schemas.Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_conversation(
    conversation_id: str,
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
):
    return await services.ChatService.conversation_delete(
        conversation_id, current_user.id
    )
