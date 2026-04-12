from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from ..database.base import Base


class Internship(Base):
    __tablename__ = "internships"
    __table_args__ = (
        CheckConstraint("mode IN ('Online', 'Offline')", name="ck_internships_mode"),
    )

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    role_title = Column(String, nullable=False)
    role_description = Column(Text, nullable=False)

    required_skills = Column(Text)

    paid = Column(Boolean, default=False)
    stipend_amount = Column(Integer, nullable=True)

    mode = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
