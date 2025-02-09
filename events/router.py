from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from events import service, schemas
from database import get_async_session


router = APIRouter()

@router.post("/create", tags=["events"])
async def create_event(event: schemas.Event = Depends(), session: AsyncSession = Depends(get_async_session)):
    return await service.create_event(event, session)


@router.get("/all", tags=["events"])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    return await service.get_all_events(session)


@router.delete("/delete", tags=["events"])
async def delete_news(event_id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_event_by_id(event_id, session)


@router.put("/registration", tags=["events"])
async def registration(init_data: str, event_id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.register_at_the_event(init_data, event_id, session)
