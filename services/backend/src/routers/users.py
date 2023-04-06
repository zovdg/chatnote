from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from tortoise.contrib.fastapi import HTTPNotFoundError

from .. import schemas
from .. import auth
from .. import services

router = APIRouter()


@router.post("/register", response_model=schemas.UserOutSchema)
async def create_user(user: schemas.UserInSchema) -> schemas.UserOutSchema:
    return await services.UserService.user_create(user)


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    token = await services.AuthService.login(user)
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


@router.get(
    "/users/me",
    response_model=schemas.UserOutSchema,
    dependencies=[Depends(auth.get_current_user)],
)
async def read_users_me(
    current_user: schemas.UserOutSchema = Depends(auth.get_current_user),
):
    return current_user


@router.delete(
    "/user/{user_id}",
    response_model=schemas.Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_user(
    user_id: str, current_user: schemas.UserOutSchema = Depends(auth.get_current_user)
) -> schemas.Status:
    return await services.UserService.user_delete(user_id, current_user.id)
