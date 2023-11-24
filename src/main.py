from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.models import User
from auth.base_config import current_user

from tests_of_candidates.router import router as router_test_candidates
from pages.router import router as pages_router

from fastapi.responses import RedirectResponse


from fastapi import Depends



app = FastAPI(
    title="Online Recruitment Platform"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


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
async def custom_404_handler(request, __):  #not_found
    return templates.TemplateResponse("404.html", {"request": request})


@app.exception_handler(401)
async def custom_401_handler(request, __): #unauthorized
    return RedirectResponse("http://127.0.0.1:8000/pages/login")
