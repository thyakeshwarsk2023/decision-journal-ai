from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from core.jwt import verify_token
from app.database import SessionLocal
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    print("TOKEN:", token)

    payload = verify_token(token)

    print("PAYLOAD:", payload)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload.get("sub")

    print("EMAIL:", email)

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    print("USER:", user)

    db.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user