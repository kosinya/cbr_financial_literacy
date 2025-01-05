from pydantic import BaseModel, Field


class User(BaseModel):
    initData: str = Field(...)
    surname: str = Field(...)
    name: str = Field(...)
    patronymic: str = Field(...)
    age: int = Field(...)
    region: str = Field(...)
