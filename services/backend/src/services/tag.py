from typing import Optional, List

from tortoise.exceptions import DoesNotExist

from ..db import models
from .. import schemas
from .. import exceptions


class TagService:
    """Tag Service."""

    @staticmethod
    async def tag_list(user_id: Optional[str] = None):
        model = models.Tags
        if user_id:
            model = model.filter(user_id=user_id)
        return await schemas.TagOutSchema.from_queryset(model.all())

    @staticmethod
    async def tag_get(tag_id) -> schemas.TagOutSchema:
        return await schemas.TagOutSchema.from_queryset_single(
            models.Tags.get(id=tag_id)
        )

    @staticmethod
    async def tag_create(tag, current_user) -> schemas.TagOutSchema:
        tag_dict = tag.dict(exclude_unset=True)
        tag_dict["user_id"] = current_user.id
        tag_obj = await models.Tags.create(**tag_dict)
        return await schemas.TagOutSchema.from_tortoise_orm(tag_obj)

    @staticmethod
    async def tag_delete(tag_id, current_user) -> schemas.Status:
        try:
            db_tag = await schemas.TagOutSchema.from_queryset_single(
                models.Tags.get(id=tag_id)
            )
        except DoesNotExist:
            raise exceptions.not_found(f"Tag {tag_id} not found")

        if db_tag.user.id == current_user.id:
            deleted_count = await models.Tags.filter(id=tag_id).delete()
            if not deleted_count:
                raise exceptions.not_found(f"Tag {tag_id} not found")
            return schemas.Status(message=f"Deleted tag {tag_id}")

        raise exceptions.forbidden(f"Not authorized to delete Tag {tag_id}")

    @staticmethod
    async def tag_conversation_list(tag_id: str) -> List[schemas.ConversationOutSchema]:
        return await schemas.ConversationOutSchema.from_queryset(
            models.Tags.get(id=tag_id).conversations.all()
        )
