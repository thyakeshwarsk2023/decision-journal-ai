from app.database import engine
from models.user import Base

Base.metadata.create_all(bind=engine)

print("Tables Created")