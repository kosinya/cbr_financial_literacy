from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from urllib import parse

from user import model, schemas


def init_data_parsing(init_data: str):
    try:
        decoded_data = parse.unquote(init_data)
        data_dict = dict(item.split('=') for item in decoded_data.split('&'))
        user = json.loads(data_dict['user'])
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Init_data string is not valid")
    return user


async def checking_registration(tg_id: int, session: AsyncSession):
    result = await session.execute(select(model.User).filter_by(tg_id=tg_id))
    user = result.scalars().first()
    if not user:
        return False
    return user


async def login(init_data: str, session: AsyncSession):
    user_data = init_data_parsing(init_data)
    user = await checking_registration(user_data['id'], session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"The user with tg_id = {user_data['id']} is not registered")
    return user


async def registration(user_data: schemas.User = Depends(), session: AsyncSession = None):
    parsed_data = init_data_parsing(user_data.initData)
    user = await checking_registration(parsed_data['id'], session)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with tg_id = {user.tg_id} is already registered")

    new_user = model.User(
        tg_id=parsed_data['id'],
        surname=user_data.surname,
        name=user_data.name,
        patronymic=user_data.patronymic,
        age=user_data.age,
        region=user_data.region,
        is_admin=False,
        is_active=True
    )
    session.add(new_user)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return new_user
