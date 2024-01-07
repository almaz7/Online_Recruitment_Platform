from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Request
from sqlalchemy import select, insert, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from loguru import logger
import os

from auth.models import User
from auth.base_config import current_user
from database import get_async_session

from tests_of_candidates.models import test_result, test, test_question, test_answer
from tests_of_candidates.schemas import Test_Result_Create

router = APIRouter(
    prefix="/test_candidate",
    tags=["Test_candidate"]
)


@router.get("/result/")
async def get_candidate_test_result_by_test_name(test_name: str = 'AIZENKA', user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    # query = (
    #     select(test_result).
    #     where(and_(test_result.c.test_id == test_id,
    #                test_result.c.user_id == user.id)).order_by(test_result.c.date).limit(1)
    # )
    # q_result = await session.execute(query)
    q_result = await session.execute(text(f"SELECT tr.id, test_id, user_id, date, result, description, test_name "
                                          f"FROM test_result tr JOIN test t ON t.id = tr.test_id WHERE t.test_name='{test_name}'"))
    result = []
    for r in q_result:
        d = {}
        d["id"] = r[0]
        d["test_id"] = r[1]
        d["user_id"] = r[2]
        d["date"] = r[3]
        d["result"] = r[4]
        d["description"] = r[5]
        d["test_name"] = r[6]
        result.append(d)

    # result = [dict(r._mapping) for r in q_result]
    if result == []:
        return {
            "status": "success",
            "data": test_name,
            "details": "no_data"
        }

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


@router.get("/test/")
async def get_test_questions_by_test_name(test_name: str = 'AIZENKA', user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = (
        select(test.c.id).
        where(test.c.test_name == test_name)
    )
    q_result = await session.execute(query)

    if q_result.rowcount == 0:
        return {
            "status": "success",
            "data": test_name,
            "details": "no_data"
        }

    test_id = q_result.one()[0]

    query = (
        select(test_question.c.id, test_question.c.question).
        where(test_question.c.test_id == test_id).
        order_by(test_question.c.id.asc())
    )
    q_result = await session.execute(query)

    if q_result.rowcount == 0:
        return {
            "status": "success",
            "data": test_name,
            "details": "no_data"
        }

    result = []
    for num, r in enumerate(q_result):
        d = {}
        d["test_name"] = test_name
        d["test_id"] = test_id
        d["user_id"] = user.id
        d["question_num"] = num + 1
        d["question_id"] = r[0]
        d["question"] = r[1]
        result.append(d)

    return {
        "status": "success",
        "data": result,
        "details": None
    }

@router.post("/test")
async def push_answers_on_test(request: Request, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    r = await request.json()
    test_id = r.pop("test_id")
    user_id = r.pop("user_id")
    test_name = r.pop("test_name")
    num = 1
    d = {}
    for question_id, answer in r.items():
        q_id = int(question_id)
        stmt = (
            insert(test_answer).values(test_id=test_id, user_id=user_id, answer_num=num, question_id=q_id, answer=answer)
        )
        d[num] = answer
        await session.execute(stmt)
        await session.commit()
        num += 1

    if str(test_name) == 'AIZENKA':
        extraversion = 0
        neuroticism = 0
        lie = 0
        for n, answer in d.items():
            if str(answer) == 'y' and (n in [1, 3, 8, 10, 13, 17, 22, 25, 27, 39, 44, 46, 49, 53, 56]):
                extraversion += 1
            elif str(answer) == 'n' and (n in [5, 15, 20, 29, 32, 34, 37, 41, 51]):
                extraversion += 1

            if str(answer) == 'y' and (n in [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43,
                                             45, 47, 50, 52, 55, 57]):
                neuroticism += 1

            if str(answer) == 'y' and (n in [6, 24, 36]):
                lie += 1
            elif str(answer) == 'n' and (n in [12, 18, 30, 42, 48, 54]):
                lie += 1

        stmt = (
            insert(test_result).values(test_id=test_id, user_id=user_id, result=extraversion, description='Экстраверсия')
        )
        await session.execute(stmt)
        await session.commit()

        stmt = (
            insert(test_result).values(test_id=test_id, user_id=user_id, result=neuroticism,
                                       description='Нейротизм')
        )
        await session.execute(stmt)
        await session.commit()

        stmt = (
            insert(test_result).values(test_id=test_id, user_id=user_id, result=extraversion,
                                       description='Шкала лжи')
        )
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