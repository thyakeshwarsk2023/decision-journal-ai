from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/decision_ai"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Connected!")