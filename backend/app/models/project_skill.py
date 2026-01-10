# backend/app/models/project_skill.py
from sqlalchemy import Column, Integer, ForeignKey
from ..database.base import Base


class Project_Skill(Base):
    __tablename__ = "project_skills"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
