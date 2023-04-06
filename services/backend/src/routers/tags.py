from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from .. import schemas
from .. import services
from .. import auth

from .. import exceptions

router = APIRouter()


@router.get(
    "/tags",
    response_model=schemas.TagOutSchemaList,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_tags(
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
):
    return await services.TagService.tag_list(current_user.id)


@router.get(
    "/tag/{tag_id}",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_tag(tag_id: str) -> schemas.TagOutSchema:
    try:
        return await services.TagService.tag_get(tag_id)
    except DoesNotExist:
        raise exceptions.not_found(f"Tag {tag_id} does not exist")


@router.post(
    "/tags",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def create_tag(
    tag: schemas.TagInSchema,
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
) -> schemas.TagOutSchema:
    return await services.TagService.tag_create(tag, current_user.id)


@router.delete(
    "/tag/{tag_id}",
    response_model=schemas.Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_tag(
    tag_id: str, current_user: schemas.UserOutSchema = Depends(auth.get_current_user)
):
    return await services.TagService.tag_delete(tag_id, current_user.id)


@router.get(
    "/tag/{tag_id}/conversations",
    response_model=schemas.ConversationOutSchemaList,
    dependencies=[Depends(auth.get_current_user)],
)
async def get_tag_conversations(tag_id: str) -> schemas.ConversationOutSchemaList:
    conversations = await services.TagService.tag_conversation_list(tag_id)
    return schemas.ConversationOutSchemaList(conversations=conversations)
