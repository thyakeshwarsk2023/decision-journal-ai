from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReflectionCreate(BaseModel):
    reflection_text :str

class ReflectionResponse(BaseModel):
    id :int
    decision_id : int
    reflection_text : str
    ai_summary : Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
