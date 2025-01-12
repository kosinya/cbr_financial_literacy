import os
from datetime import datetime
from fastapi import HTTPException, status, File, UploadFile
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import config
import utils
from surveys import model
from user import service as user_service


async def get_all_surveys(session: AsyncSession):
    result = await session.execute(select(model.Survey))
    return result.scalars().all()


async def get_survey_by_id(session: AsyncSession, survey_id: int):
    result = await session.execute(select(model.Survey).where(model.Survey.id == survey_id))
    result = result.scalars().first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found")

    filepath = os.path.join(config.FILES_DIR, result.filename)
    text = utils.read_file(filepath)
    return utils.string_to_json(text)

# TODO: Добавить функцию вычисления итогового результата
async def saving_the_result(init_data: str, survey_id: int, session: AsyncSession):
    user = await user_service.login(init_data, session)
    survey = await get_survey_by_id(session, survey_id)

    new_result = model.Result(
        survey_id=survey_id,
        user_id=user.id,
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        # FIXME
        score=100
    )
    session.add(new_result)

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return new_result


# TODO: Переписать с join
async def get_passed_tests(init_test: str, session: AsyncSession):
    user = await user_service.login(init_test, session)
    result = await session.execute(select(model.Result.survey_id).distinct(model.Result.survey_id).where(model.Result.user_id == user.id))
    passed_test_ids = result.scalars().all()

    passed_tests = await session.execute(select(model.Survey).where(model.Survey.id.in_(passed_test_ids)))
    return passed_tests.scalars().all()


async def get_test_results(init_test: str, survey_id: int, session: AsyncSession):
    user = await user_service.login(init_test, session)
    result = await session.execute(select(model.Result).
                                   where(model.Result.survey_id == survey_id, model.Result.user_id == user.id))
    result = result.scalars().all()
    return result
