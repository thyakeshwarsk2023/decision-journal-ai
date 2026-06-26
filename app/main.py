from fastapi import     FastAPI
from routes.auth import router
from models.user import User
from models.decision import Decision
from app.database import Base, engine
from models.decision import Decision

Decision.__table__.drop(bind=engine)
Decision.__table__.create(bind=engine)
app = FastAPI()
app.include_router(router)
@app.get("/")

def home():
    return {"message": "Decision Journal API"}
from sqlalchemy import inspect


@app.get("/tables")
def tables():

    inspector = inspect(engine)

    return inspector.get_table_names()
from routes.decisions import router as decision_router
app.include_router(router)
app.include_router(decision_router)
from sqlalchemy import inspect

@app.get("/decision-columns")
def decision_columns():
    inspector = inspect(engine)

    return [
        col["name"]
        for col in inspector.get_columns("decisions")
    ]
