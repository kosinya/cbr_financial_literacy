from pydantic import BaseModel, Field


class User(BaseModel):
    tg_id: int = Field(...)
    surname: str = Field(...)
    name: str = Field(...)
    patronymic: str = Field(...)
    tg_username: str = Field(...)
    age: int = Field(...)
    region: str = Field(...)
