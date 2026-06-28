from fastapi import (
    APIRouter,
    Depends
)

from app.database import SessionLocal
from core.dependencies import get_current_user

from models.user import User
from models.decision import Decision


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/confidence-calibration")
def confidence_calibration(
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    decisions = (
        db.query(Decision)
        .filter(
            Decision.user_id == current_user.id,
            Decision.outcome_rating != None
        )
        .all()
    )

    data = []

    for decision in decisions:

        diff = abs(
            decision.confidence_score
            -
            decision.outcome_rating
        )

        data.append({
            "title": decision.title,
            "confidence": decision.confidence_score,
            "outcome": decision.outcome_rating,
            "error": diff
        })

    db.close()

    return data


@router.get("/gut-vs-logic")
def gut_vs_logic(
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    decisions = (
        db.query(Decision)
        .filter(
            Decision.user_id == current_user.id,
            Decision.outcome_rating != None
        )
        .all()
    )

    gut_scores = []
    logic_scores = []

    for decision in decisions:

        if decision.gut_logic_score >= 6:

            gut_scores.append(
                decision.outcome_rating
            )

        else:

            logic_scores.append(
                decision.outcome_rating
            )

    gut_avg = (
        sum(gut_scores) / len(gut_scores)
        if gut_scores else 0
    )

    logic_avg = (
        sum(logic_scores) / len(logic_scores)
        if logic_scores else 0
    )

    db.close()

    return {
        "gut_average": round(gut_avg, 2),
        "logic_average": round(logic_avg, 2)
    }


@router.get("/future-feelings")
def future_feelings(
    current_user: User = Depends(get_current_user)
):

    db = SessionLocal()

    decisions = (
        db.query(Decision)
        .filter(
            Decision.user_id == current_user.id,
            Decision.outcome_rating != None
        )
        .all()
    )

    analysis = []

    for decision in decisions:

        prediction = decision.future_feeling

        actual = (
            "proud"
            if decision.outcome_rating >= 7
            else "regret"
        )

        analysis.append({
            "title": decision.title,
            "predicted": prediction,
            "actual": actual,
            "correct": prediction == actual
        })

    db.close()

    return analysis