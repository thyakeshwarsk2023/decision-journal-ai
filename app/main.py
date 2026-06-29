from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Import models so SQLAlchemy registers them
from models.user import User
from models.decision import Decision
from models.reflection import Reflection

from routes.auth import router as auth_router
from routes.decisions import router as decision_router
from routes.reflections import router as reflection_router
from routes.analytics import router as analytics_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(decision_router)
app.include_router(reflection_router)
app.include_router(analytics_router)


@app.get("/")
def home():
    return {
        "message": "Decision Journal API"
    }