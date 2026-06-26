from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DecisionCreate(BaseModel):
    title : str
    decision_text : str

    category : str

    mood_score : int

    confidence_score : int

    gut_logic_score : int

    future_feeling: str

    days_to_decide: int

class OutcomeUpdate(BaseModel):
    outcome_rating: int

class DecisionResponse(BaseModel):
    id :int
    user_id: int
    title: str
    decision_text: str
    category: str

    mood_score: int

    confidence_score: int
    gut_logic_score: int

    future_feeling: str

    days_to_decide: int

    outcome_rating: Optional[int]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



             



