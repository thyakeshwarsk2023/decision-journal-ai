from fastapi import APIRouter
from core.security import hash_password
from schemas.user import UserCreate
from models.user import User
from app.database import SessionLocal
from core.security import verify_password
from core.jwt import create_access_token
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
@router.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    response = {
        "message": "User created",
        "id": new_user.id
    }

    db.close()
    return response

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm= Depends()
):
    email = form_data.username
    password = form_data.password
    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter((User.email == email))
        .first()
    )
    if not db_user:
        raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )

    if not verify_password(password, db_user.password):
        raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )
    token = create_access_token(
        {"sub": db_user.email}
    )
    db.close()
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/users")
def get_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()
    return [
        {
        "id": user.id,
        "username": user.username,
         "email": user.email
        }
        for user in users
    ]

from fastapi import Depends
from core.dependencies import get_current_user

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }
from fastapi import Header
from core.jwt import verify_token

from fastapi import Header

@router.get("/test-jwt")
def test_jwt(
    authorization: str = Header(None)
):
    print("AUTH HEADER:", authorization)

    if authorization is None:
        return {"error": "No header received"}

    token = authorization.replace("Bearer ", "")

    payload = verify_token(token)

    return payload
@router.get("/protected-test")
def protected_test(
    current_user = Depends(get_current_user)
):
    return {
        "message": "Authentication working",
        "email": current_user.email
    }
@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"message": "User not found"}

    db.delete(user)
    db.commit()

    db.close()

    return {"message": "Deleted"}
@router.get("/headers")
def headers(
    authorization: str = Header(None)
):
    return {
        "authorization": authorization
    }

from core.jwt import verify_token


@router.get("/force-user")
def force_user(token: str):

    payload = verify_token(token)

    if payload is None:
        return {"error": "Invalid token"}

    email = payload.get("sub")

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    db.close()

    if not user:
        return {"error": "User not found"}

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }