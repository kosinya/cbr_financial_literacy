import os
import json
import aiofiles
from fastapi import HTTPException, status, File, UploadFile
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import config
import utils
from surveys import model


async def get_all_surveys(session: AsyncSession):
    result = await session.execute(select(model.Survey))
    return result.scalars().all()


async def get_survey_bu_id(session: AsyncSession, survey_id: int):
    result = await session.execute(select(model.Survey).where(model.Survey.id == survey_id))
    result = result.scalars().first()

    filepath = os.path.join(config.FILES_DIR, result.filename)
    text = utils.read_file(filepath)
    return utils.string_to_json(text)
