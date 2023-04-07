from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from .. import schemas
from ..auth import get_current_user
from ..services import users as user_service
from ..services import auth as auth_service

router = APIRouter()

auth_router = APIRouter()

@auth_router.post("/register", response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn) -> schemas.UserOut:
    return await user_service.create_user(user)


@auth_router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    token = await auth_service.login(user)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="lax",
        secure=False,
    )
    return response

user_router = APIRouter()


@user_router.get(
    "/users/me",
    response_model=schemas.UserOut,
    dependencies=[Depends(get_current_user)],
)
async def read_users_me(
    current_user: schemas.UserOut = Depends(get_current_user),
):
    return current_user


router.include_router(auth_router, tags=['auth'])
router.include_router(user_router, tags=['user'])
