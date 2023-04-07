from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from jose import jwt, JWTError
from tortoise.exceptions import DoesNotExist

from ..core.config import settings
from ..schemas.token import TokenData
from ..schemas.users import UserOut
from ..db.models import Users

from .. import exceptions


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise exceptions.unauthorized("Not authenticated")
            else:
                return None

        return param


security = OAuth2PasswordBearerCookie(token_url="/login")


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exceptions.unauthorized("Could not validate credentials")
        token_data = TokenData(username=username)
    except JWTError:
        raise exceptions.unauthorized("Could not validate credentials")

    try:
        user = await UserOut.from_queryset_single(
            Users.get(username=token_data.username)
        )
    except DoesNotExist:
        raise exceptions.unauthorized("Could not validate credentials")

    return user
