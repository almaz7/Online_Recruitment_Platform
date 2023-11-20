from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates

from tests_of_candidates.router import get_candidate_test_result_by_type
from auth.auth_router import user_login


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates/public")

@router.get("/base")
async def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/login") #dependencies=[Depends(user_login)]
async def login_user(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login") #dependencies=[Depends(user_login)]
async def login_user(request: Request, result=Depends(user_login)):
    return result


@router.get("/test_results/{user_id}")
async def get_search_page(request: Request, results=Depends(get_candidate_test_result_by_type)):
    return templates.TemplateResponse("search.html", {"request": request, "results": results["data"]})




