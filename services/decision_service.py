from fastapi import HTTPException
from models.decision import Decision

def get_user_decision(
        db,
        decision_id: int,
        user_id: int
):
    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == user_id
        )
        .first()
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )
    return Decision
    