from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from auth.models import User
from auth.base_config import current_user
from database import get_async_session

from tests_of_candidates.models import test_candidate
from tests_of_candidates.schemas import Test_Candidate_Create, Test_Candidate_Get

router = APIRouter(
    prefix="/test_candidate",
    tags=["Test_candidate"]
)


@router.get("/result", response_model=list[Test_Candidate_Get])
async def get_candidate_test_result(result_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(test_candidate).where(test_candidate.c.result_type == result_type)
    result = await session.execute(query)
    # return result.all()
    return [dict(r._mapping) for r in result]


@router.post("/result")
async def add_candidate_test_result(new_candidate_test_result: Test_Candidate_Create, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = insert(test_candidate).values(**new_candidate_test_result.dict(), user_id=user.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/get_aizenka_test")
async def download_file():
    return FileResponse(path='./test_documents/AIZENKA.xlsx', filename='Тест_Айзенка.xlsx', media_type='multipart/form-data')


@router.post("/upload_aizenka_test")
async def upload_file(file: UploadFile):

    return {"status": "success", "uploaded file":str(file.filename)}