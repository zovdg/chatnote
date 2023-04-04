from tortoise.contrib.pydantic import pydantic_model_creator

from ..db.models import Tags

TagInSchema = pydantic_model_creator(
    Tags, name="TagIn", exclude=("user_id",), exclude_readonly=True
)
TagOutSchema = pydantic_model_creator(Tags, name="Tag")
