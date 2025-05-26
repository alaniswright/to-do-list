# Defines request and response models.
# Used to validate and parse input data (from JSON requests).
# Also shapes the data returned to clients (response models).

from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    published: Optional[bool] = True