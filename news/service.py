import os
import json
import aiofiles
from fastapi import HTTPException, status, File, UploadFile
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import config
from news import model, schemas

async def create_news(news: schemas.News, image: UploadFile = File(...), session: AsyncSession = None):
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail='File must be an image')

    folder = os.path.join(config.STATIC_DIR, 'images')
    os.makedirs(folder, exist_ok=True)

    image_path = os.path.join(folder, image.filename)
    async with aiofiles.open(image_path, 'wb') as out:
        content = await image.read()
        await out.write(content)

    new_article = model.News(
        title=news.title,
        description=news.description,
        content=news.content,
        image_url=config.STATIC_DIR + '/images/' + image.filename,
        is_event=news.is_event,
        tags=','.join(news.tags),
    )

    session.add(new_article)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "title": news.title,
        "description": news.description,
        "content": news.content,
        "image_url": new_article.image_url,
        "is_event": news.is_event,
    })


async def get_all_news(session: AsyncSession):
    news = await session.execute(select(model.News))
    return news.scalars().all()