from typing import Optional

from fastapi import HTTPException, status


def unauthorized(detail: Optional[str] = None):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail or "Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden(detail: Optional[str] = None):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail=detail or "Forbidden"
    )


def not_found(detail: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )
