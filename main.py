import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import config
from user.router import router as user_router
from news.router import router as news_router
from surveys.router import router as surveys_router


app = FastAPI()
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")

@app.get('/')
async def welcome():
    return {'message': 'Welcome to CBR Financial Literacy App!'}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix='/auth')
app.include_router(news_router, prefix='/news')
app.include_router(surveys_router, prefix='/surveys')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
