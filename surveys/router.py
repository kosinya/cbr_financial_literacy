from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from surveys import service
from database import get_async_session

router = APIRouter()


@router.get("/all", tags=["surveys"])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    return await service.get_all_surveys(session)

@router.get("/get_by_id", tags=["surveys"])
async def get_survey_by_id(survey_id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_survey_by_id(session, survey_id)


@router.post("/save_result", tags=["surveys"])
async def save_the_result(init_data: str, survey_id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.saving_the_result(init_data, survey_id, session)


@router.get("/passed_tests", tags=["surveys"])
async def get_passed_tests(init_data: str, session: AsyncSession = Depends(get_async_session)):
    return await service.get_passed_tests(init_data, session)


@router.get("/get_test_result", tags=["surveys"])
async def get_test_result(init_data: str, survey_id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_test_results(init_data, survey_id, session)
