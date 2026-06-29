from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.orm import relationship





class Decision(Base):
    __tablename__ = "decisions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    title = Column(
        String,
        nullable=False
    )
    decision_text = Column(
    Text,
    nullable=False
    )

    category = Column(
        String,
        nullable=False
    )
    mood_score = Column(
        Integer,
        nullable=False
    )
    confidence_score = Column(
        Integer,
        nullable=False
    )
    gut_logic_score = Column(
        Integer,
        nullable=False
    )
    future_feeling = Column(
        String,
        nullable=False
    )
    days_to_decide = Column(
        Integer,
        nullable=False
    )

    # Added later by user
    outcome_rating = Column(
        Integer,
        nullable=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    user = relationship(
    "User",
    back_populates="decisions"
    )
    reflections = relationship(
    "Reflection",
    back_populates="decision"
    )
   
    






