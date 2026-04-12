from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from ..database.base import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("difficulty IN ('Easy', 'Medium', 'Hard')", name="ck_projects_difficulty"),
        CheckConstraint("status IN ('Idea', 'Ongoing', 'Completed')", name="ck_projects_status"),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    members_count = Column(Integer)
    student_role = Column(Text, nullable=False)

    difficulty = Column(String)
    status = Column(String)

    outcome = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
