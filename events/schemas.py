from pydantic import BaseModel, Field
from typing import List, Optional

class Event(BaseModel):
    title: str = Field(...)
    date: str = Field(...)
    tags: Optional[List[str]] = Field(None)
