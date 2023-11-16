from fastapi import FastAPI

from auth.models import User
from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from fastapi import Depends
from tests_of_candidates.router import router as router_operation

app = FastAPI(
    title="Online Recruitment Platform"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    
    return f"Hello, {user.username}. You registered at {user.registered_at}"



@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"