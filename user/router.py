from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from user import service, schemas
from database import get_async_session
router = APIRouter()


@router.get("/login", tags=["auth"])
async def login(init_data: str, session: AsyncSession = Depends(get_async_session)):
    return await service.login(init_data=init_data, session=session)


@router.post('/registration', tags=["auth"])
async def registration(user_data: schemas.User, session: AsyncSession = Depends(get_async_session)):
    res = await service.registration(user_data, session)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=res)
