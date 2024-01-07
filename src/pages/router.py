from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from tests_of_candidates.router import get_candidate_test_result_by_test_name, get_test_questions_by_test_name
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from auth.models import User
from auth.base_config import current_user

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
async def get_search_page(request: Request, results=Depends(get_candidate_test_result_by_test_name)):
    return templates.TemplateResponse("test_result.html",
                                      {"request": request, "results": results["data"], "details": results["details"]})


@router.get("/video_interview")
async def get_user_video(request: Request, duration: int = 6, user: User = Depends(current_user)):
    return templates.TemplateResponse("video_stream.html", {"request": request, "duration": duration})


@router.get("/test/")
async def get_test_questions(request: Request, test_questions=Depends(get_test_questions_by_test_name)):
    return templates.TemplateResponse("test.html",
                                      {"request": request, "results": test_questions["data"], "details": test_questions["details"]}
                                      )

