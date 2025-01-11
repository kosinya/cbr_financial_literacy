from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from surveys import service
from database import get_async_session


router = APIRouter()


@router.get("/all", tags=["surveys"])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    return await service.get_all_surveys(session)

@router.get("/{id}", tags=["surveys"])
async def get_survey_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_survey_bu_id(session, id)