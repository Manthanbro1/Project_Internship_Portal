# backend/app/models/skill.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database.base import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
