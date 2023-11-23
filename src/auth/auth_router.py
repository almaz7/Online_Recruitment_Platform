from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_users import models
from fastapi_users.authentication import Authenticator, AuthenticationBackend, Strategy
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.router.common import ErrorCode
from auth.manager import get_user_manager
from auth.base_config import auth_backend
router = APIRouter()
#не используется, берется из дефолтный документации
@router.post(
    "/login",
    tags=["user_login"],
)
async def user_login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )

    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response