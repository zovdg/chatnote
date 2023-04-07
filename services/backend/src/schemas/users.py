from tortoise.contrib.pydantic import pydantic_model_creator

from ..db import models as db_models


UserIn = pydantic_model_creator(db_models.Users, name="UserIn", exclude_readonly=True)
UserOut = pydantic_model_creator(
    db_models.Users, name="UserOut", exclude=("password", "created_at", "updated_at")
)
UserDB = pydantic_model_creator(
    db_models.Users, name="UserDB", exclude=("created_at", "updated_at")
)
