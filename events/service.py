from fastapi import HTTPException, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from events import model, schemas
from user import service as user_service

async def get_all_events(session: AsyncSession):
    news = await session.execute(select(model.Event))
    return news.scalars().all()


async def create_event(event: schemas.Event, session: AsyncSession = None):
    new_event = model.Event(
        title=event.title,
        date=event.date,
        number_of_participants=0,
        participant_ids="",
        tags=",".join(event.tags)
    )

    session.add(new_event)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "title": new_event.title,
        "date": new_event.date,
        "number_of_participants": new_event.number_of_participants,
        "participant_ids": new_event.participant_ids,
        "tags": new_event.tags
    })


async def delete_event_by_id(event_id: int, session: AsyncSession):
    result = await session.execute(select(model.Event).where(model.Event.id == event_id))
    event = result.scalars().first()

    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event with id = {event_id} not found')

    await session.delete(event)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f'Event with id = {event_id} deleted'}


async def register_at_the_event(init_data: str, event_id: int, session: AsyncSession):
    user = user_service.init_data_parsing(init_data)

    event = await session.execute(select(model.Event).where(model.Event.id == event_id))
    event = event.scalars().first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event with id = {event_id} not found')

    list_ids = event.participant_ids.split(',')
    if str(user["id"]) in list_ids:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with id = {user["id"]} already registered')

    event.participant_ids += str(user["id"]) + ','
    event.number_of_participants += 1

    session.add(event)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"success": True}
