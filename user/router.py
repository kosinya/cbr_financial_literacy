from fastapi import APIRouter, status
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/auth", tags=["user"])
def user_auth(init_data: str):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": {"username": init_data}})
