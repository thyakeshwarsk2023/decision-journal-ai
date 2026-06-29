from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from sqlalchemy.orm import Session
from core.dependencies import get_current_user

from models.user import User
from models.decision import Decision

from schemas.decision import (
    DecisionCreate,
    DecisionResponse,
    OutcomeUpdate
)
router = APIRouter(
    prefix="/decisions",
    tags=["Decisions"]
)
@router.post(
    "",
    response_model=DecisionResponse
)
def create_decision(
    decision: DecisionCreate,
    current_user: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):


       new_decision = Decision(

        user_id=current_user.id,

        title=decision.title,
        decision_text=decision.decision_text,

        category=decision.category,

        mood_score=decision.mood_score,
        confidence_score=decision.confidence_score,

        gut_logic_score=decision.gut_logic_score,

        future_feeling=decision.future_feeling,

        days_to_decide=decision.days_to_decide
        )
       db.add(new_decision)
       db.commit()
       db.refresh(new_decision)
       return new_decision
@router.get(
    "",
    response_model=list[DecisionResponse]
)
def get_decisions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    decisions = (
        db.query(Decision)
        .filter(
            Decision.user_id == current_user.id
        )
        .all()
    )

   

    return decisions
@router.get(
    "/{decision_id}",
    response_model=DecisionResponse
)
def get_decision(
    decision_id: int,
    current_user: User = Depends(get_current_user),
      db: Session = Depends(get_db)
):

    

    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == current_user.id
        )
        .first()
    )

    

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    return decision
@router.patch(
    "/{decision_id}/outcome",
    response_model=DecisionResponse
)
def update_outcome(
    decision_id: int,
    outcome: OutcomeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

   
    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == current_user.id
        )
        .first()
    )

    if not decision:

       

        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    decision.outcome_rating = outcome.outcome_rating

    db.commit()

    db.refresh(decision)


    return decision
@router.delete("/{decision_id}")
def delete_decision(
    decision_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    

    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == current_user.id
        )
        .first()
    )

    if not decision:
        

        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )

    db.delete(decision)

    db.commit()

   

    return {
        "message": "Decision deleted successfully"
    }
