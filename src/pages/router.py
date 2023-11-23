from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from tests_of_candidates.router import get_candidate_test_result_by_type
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates/public")


@router.get("/base")
async def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/login")
async def login_user(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["Auth"]
)


@router.get("/register")
async def login_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["Auth"],
)


@router.get("/test_results/")
async def get_search_page(request: Request, results=Depends(get_candidate_test_result_by_type)):
    return templates.TemplateResponse("search.html", {"request": request, "results": results["data"]})




