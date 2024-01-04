import datetime
import sys
import traceback

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse


from loguru import logger
import os

from auth.models import User
from auth.base_config import current_user
from database import get_async_session

from videos_of_candidates.models import video_candidate
from videos_of_candidates.schemas import Video_Candidate_Create, Video_Candidate_Get

router = APIRouter(
    prefix="/video_candidate",
    tags=["Video_candidate"]
)


@router.get("/get_videos")
async def get_candidate_videos(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = (
        select(video_candidate).
        where(
            video_candidate.c.user_id == user.id
        )
    )
    q_result = await session.execute(query)
    result = [dict(r._mapping) for r in q_result]
    return {
        "status": "success",
        "data": result,
        "details": None
    }

# import requests

sys.path.append(os.path.join(sys.path[0], 'video_records'))
@router.post("/add_video")
async def add_candidate_video(question_id: int, file: UploadFile, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        if not os.path.exists(f"video_records/{user.email}"):
            os.mkdir(f"video_records/{user.email}")
        if not os.path.exists(f"video_records/{user.email}/{question_id}"):
            os.mkdir(f"video_records/{user.email}/{question_id}")
        time = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        path = f"video_records/{user.email}/{question_id}/{time}.mp4"

        async with aiofiles.open(path,"wb") as video_trg_file:
            content = await file.read()
            await video_trg_file.write(content)
        stmt = insert(video_candidate).values(question_id=question_id, user_id=user.id, path=path)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except Exception as e:
        logger.error(str(e))
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при добавлении видеозаписи интервью")
#
#
# @router.get("/get_aizenka_test")
# async def download_file(user: User = Depends(current_user)):
#     logger.info(f"user_id = {user.id}")
#     file_path = "test_documents/AIZENKA.xlsx"
#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Нет файла с таким путем")
#     return FileResponse(path=file_path, filename='Тест_Айзенка.xlsx', media_type='multipart/form-data')
#
#
# @router.post("/upload_aizenka_test")
# async def upload_file(file: UploadFile, user: User = Depends(current_user)):
#     if not file.filename.endswith(".xlsx"):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат файла: файл должен быть в формате .xlsx")
#     return {
#         "status": "success",
#         "data": None,
#         "details": {"uploaded file": str(file.filename)}
#     }