from fastapi import APIRouter
from core.security import hash_password
from schemas.user import UserCreate
from models.user import User
from app.database import SessionLocal
from schemas.login import LoginRequest
from core.security import verify_password
from core.jwt import create_access_token
from fastapi import HTTPException
router = APIRouter()
@router.post("/register")

def register(user:UserCreate):
    db = SessionLocal()
    hashed_password = hash_password(
        user.password
    )
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
def login(user: LoginRequest):
    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter((User.email == user.email))
        .first()
    )
    if not db_user:
        raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )
    token = create_access_token(
        {"sub": db_user.email}
    )
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
@router.get("/secret")

def  secret():
    return {
        "message":"Protected data"
    }
from fastapi import Depends
from core.dependencies import get_current_user

from fastapi import Depends
from core.dependencies import get_current_user

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }
from fastapi import Header

@router.get("/test-token")
def test_token(authorization: str = Header()):
    return {"token": authorization}
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
@router.get("/debug-jwt")
def debug_jwt(token: str):
    return {
        "token": token,
        "length": len(token)
    }
@router.get("/force-decode")
def force_decode(token: str):
    return verify_token(token)
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
@router.get("/protected-test")
def protected_test(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
@router.get("/force-user")
def force_user(token: str):
    payload = verify_token(token)

    email = payload["sub"]

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }