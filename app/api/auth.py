from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from typing import Annotated
from ..config import get_auth_service
from ..env_vars import ENV_VARS
from ..managers.auth_manager import AuthManager

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def authenticate_user(
    request: Request,
    response: Response,
    auth_service: Annotated[AuthManager, Depends(get_auth_service)]
) -> dict:
    try:
        body = await request.json()
        secret = body["secret"]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Missing <secret> field.")

    if not auth_service.verify_secret(secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect app secret.")

    token = auth_service.generate_token()
    response.set_cookie(
        key=ENV_VARS.get("JWT_COOKIE"),
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=int(auth_service.exp_time * 60 * 60)  # exp_time in hours, max_age takes seconds
    )

    return { "message": "Authenticated." }
