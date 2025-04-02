from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import ValidationError
from typing import Annotated
from ..config import get_auth_service
from ..managers.auth_manager import AuthManager

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def authenticate_user(
    request: Request,
    auth_service: Annotated[AuthManager, Depends(get_auth_service)]
) -> None:
    try:
        body = await request.json()
        secret = body["secret"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Missing <secret> field.")

    if not auth_service.verify_secret(secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect app secret.")

    token = auth_service.generate_token()
    # TODO set token in cookie n implement a middleware
