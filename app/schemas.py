from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    published: Optional[bool] = True

class TaskComplete(BaseModel):
    id: int