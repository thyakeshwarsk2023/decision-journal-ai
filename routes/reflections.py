from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.database import SessionLocal

from models.user import User
from models.decision import Decision
from models.reflection import Reflection

from schemas.reflection import (
    ReflectionCreate,
    ReflectionResponse
)
from services.ai_reflection import (
    generate_ai_reflection
)
from core.dependencies import get_current_user

router = APIRouter(
    prefix="/reflections",
    tags=["Reflections"]
)
@router.post(
    "/{decision_id}",
    response_model=ReflectionResponse
)

def create_reflection(
    decision_id : int,
    reflection: ReflectionCreate,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == current_user.id
        )
        .first()
    )
    if not decision:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )
    new_reflection = Reflection(
        decision_id = decision.id,
        reflection_text=reflection.reflection_text
    )
    db.add(new_reflection)
    db.commit()
    db.refresh(new_reflection)
    db.close()
    return new_reflection

@router.get(
    "/{decision_id}",
    response_model=list[ReflectionResponse]
)

def get_reflections(
    decision_id: int,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == current_user.id
        )
        .first()
    )
    if not decision:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Decision not found"
    )
    reflections = (
        db.query(Reflection)
        .filter(
            Reflection.decision_id == decision_id
        )
        .all()
    )
    db.close()
    return reflections

@router.post("/ai-reflect/{decision_id}")

def ai_reflect(
    decision_id: int,
    current_user: User = Depends(get_current_user)
):
    db = SessionLocal()

    decision = (
        db.query(Decision)
        .filter(
            Decision.id == decision_id,
            Decision.user_id == current_user.id
        )
        .first()
    )
    if not decision:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="Decision not found"
        )
    
    reflections = (
        db.query(Reflection)
        .filter(
            Reflection.decision_id == decision_id
        )
        .all()
    )
    reflection_texts = [
        reflection.reflection_text
        for reflection in reflections
    ]
    ai_output = generate_ai_reflection(
        decision.decision_text,
        reflection_texts
    )

    if reflections:
        reflections[-1].ai_summary = ai_output

        db.commit()

    db.close()
    return {
        "ai reflection": ai_output
    }    

