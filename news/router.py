from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from news import service, schemas
from database import get_async_session


router = APIRouter()

@router.post("/create", tags=["news"])
async def create_news(news: schemas.News = Depends(), image: UploadFile = File(...),
                      session: AsyncSession = Depends(get_async_session)):
    return await service.create_news(news, image, session)


@router.get("/all", tags=["news"])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    return await service.get_all_news(session)


@router.delete("/delete/{id}", tags=["news"])
async def delete_news(id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_news_by_id(id, session)
