from fastapi import     FastAPI
from routes.auth import router
from models.user import User
from routes.reflections import router as reflection_router
from app.database import Base, engine
from models.decision import Decision
# app/main.py
from routes.auth import router as auth_router
from models.reflection import Reflection
from routes.analytics import (
    router as analytics_router
)
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")

def home():
    return {"message": "Decision Journal API"}
from sqlalchemy import inspect


@app.get("/tables")
def tables():

    inspector = inspect(engine)

    return inspector.get_table_names()
from routes.decisions import router as decision_router
app.include_router(auth_router)
app.include_router(decision_router)
app.include_router(reflection_router)
app.include_router(analytics_router)
from sqlalchemy import inspect

@app.get("/decision-columns")
def decision_columns():
    inspector = inspect(engine)

    return [
        col["name"]
        for col in inspector.get_columns("decisions")
    ]
