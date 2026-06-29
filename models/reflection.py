from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Reflection(Base):
    __tablename__ = "reflections"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    decision_id = Column(
        Integer,
        ForeignKey("decisions.id"),
        nullable=False
    )
    reflection_text = Column(
        Text,
        nullable=False
    )
    ai_summary = Column(
        Text,
        nullable=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    decision = relationship(
    "Decision",
    back_populates="reflections"
    )