from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from .. import auth
from .. import exceptions


async def login(user: OAuth2PasswordRequestForm):
    user = await auth.validate_user(user)

    if not user:
        raise exceptions.unauthorized("Incorrect username or password")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    return jsonable_encoder(access_token)
