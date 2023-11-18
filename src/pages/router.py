from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates

from tests_of_candidates.router import get_candidate_test_result_by_type
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


@router.get("/test_results/{user_id}")
async def get_search_page(request: Request, results=Depends(get_candidate_test_result_by_type)):
    return templates.TemplateResponse("search.html", {"request": request, "results": results["data"]})


