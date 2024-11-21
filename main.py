import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def welcome():
    return {'message': 'Welcome to CBR Financial Literacy App!'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
