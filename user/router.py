from fastapi import APIRouter, status
from starlette.responses import JSONResponse
import urllib.parse
import json

router = APIRouter()


@router.post("/auth", tags=["user"])
def user_auth(init_data: str):
    decoded_data = urllib.parse.unquote(init_data)
    data_dict = dict(item.split('=') for item in decoded_data.split('&'))
    user = json.loads(data_dict['user'])
    return JSONResponse(status_code=status.HTTP_200_OK, content={"username": user.get('username')})
