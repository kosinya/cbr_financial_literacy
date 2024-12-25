from fastapi import HTTPException, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from urllib import parse

from user import model

def init_data_parsing(init_data: str):
    decoded_data = parse.unquote(init_data)
    data_dict = dict(item.split('=') for item in decoded_data.split('&'))
    user = json.loads(data_dict['user'])
    return user


async def checking_registration(tg_id: int, session: AsyncSession):
    result = await session.execute(select(model.User).filter_by(tg_id=tg_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with tg_id = {tg_id} not found")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=user)