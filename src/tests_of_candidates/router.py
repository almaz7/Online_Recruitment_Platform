from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from loguru import logger
import os

from auth.models import User
from auth.base_config import current_user
from database import get_async_session

from tests_of_candidates.models import test_result
from tests_of_candidates.schemas import Test_Result_Create

router = APIRouter(
    prefix="/test_result",
    tags=["Test_candidate"]
)


@router.get("/result/")
async def get_candidate_test_result_by_test_id(test_id: int = 1, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = (
        select(test_result).
        where(and_(test_result.c.test_id == test_id,
                   test_result.c.user_id == user.id)).order_by(test_result.c.date).limit(1)
    )
    print(query)
    q_result = await session.execute(query)
    result = [dict(r._mapping) for r in q_result]
    return {
        "status": "success",
        "data": result,
        "details": None
    }


@router.post("/result")
async def add_candidate_test_result(new_candidate_test_result: Test_Result_Create, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = insert(test_result).values(**new_candidate_test_result.dict(), user_id=user.id)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "data": None,
        "details": None
    }

#не используется в продакшн
@router.get("/get_aizenka_test")
async def download_file(user: User = Depends(current_user)):
    # logger.info(f"user_id = {user.id}")
    file_path = "test_documents/AIZENKA.xlsx"
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Нет файла с таким путем")
    return FileResponse(path=file_path, filename='Тест_Айзенка.xlsx', media_type='multipart/form-data')


#не используется в продакшн
@router.post("/upload_aizenka_test")
async def upload_file(file: UploadFile, user: User = Depends(current_user)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат файла: файл должен быть в формате .xlsx")
    return {
        "status": "success",
        "data": None,
        "details": {"uploaded file": str(file.filename)}
    }