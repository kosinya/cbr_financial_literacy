import os
import urllib
from fileinput import filename

import aiofiles
from urllib.parse import urlparse
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


async def delete_news_by_id(news_id: int, session: AsyncSession):
    result = await session.execute(select(model.News).where(model.News.id == news_id))
    news = result.scalars().first()

    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'News with id = {news_id} not found')

    # TODO: Убрать костыль, добавив поле для хранения filename
    path = urlparse(news.image_url).path
    file = path.split('/')[-1]

    if os.path.exists(os.path.join(config.STATIC_DIR, 'images', file)):
        os.remove(os.path.join(config.STATIC_DIR, 'images', file))

    await session.delete(news)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f'News with id = {news_id} deleted'}