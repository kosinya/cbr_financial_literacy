from fastapi import HTTPException, status
from starlette.responses import JSONResponse
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
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=user)


async def login(init_data: str, session: AsyncSession):
    user_data = init_data_parsing(init_data)
    print(user_data)
    user = await checking_registration(user_data['id'], session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"The user with tg_id = {user_data['id']} is not registered")
    return user


async def registration(user_data: schemas.User, session: AsyncSession):
    check = await checking_registration(user_data.tg_id, session)
    print(check)
    if check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with th_id = {user_data.tg_id} is already registered")

    new_user = model.User(
        tg_id=user_data.tg_id,
        surname=user_data.surname,
        name=user_data.name,
        patronymic=user_data.patronymic,
        tg_username=user_data.tg_username,
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

    return {
        "surname": new_user.surname,
        "name": new_user.name,
        "patronymic": new_user.patronymic,
    }
