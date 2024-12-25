from pydantic import BaseModel, Field
from typing import List, Optional

class News(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    content: str = Field(...)
    is_event: bool = Field(...)
    tags: Optional[List[str]] = Field(None)
