from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from fastapi import Depends
from tests_of_candidates.router import router as router_test_candidates
from pages.router import router as pages_router

#from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Online Recruitment Platform"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

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

app.include_router(router_test_candidates)

app.include_router(pages_router)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    
    return f"Hello, {user.username}. You registered at {user.registered_at}"



@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


templates = Jinja2Templates(directory="templates/public")
@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request})