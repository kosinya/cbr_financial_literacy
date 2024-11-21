import uvicorn
from fastapi import FastAPI

from user.router import router as UserRouter

app = FastAPI()


@app.get('/')
async def welcome():
    return {'message': 'Welcome to CBR Financial Literacy App!'}

app.include_router(UserRouter, prefix='/user')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
