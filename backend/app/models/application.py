from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from ..database.base import Base


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("student_id", "internship_id", name="uq_applications_student_internship"),
        CheckConstraint(
            "status IN ('Applied', 'Shortlisted', 'Selected', 'Rejected')",
            name="ck_applications_status",
        ),
    )

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)

    status = Column(String, default="Applied", nullable=False)
    rejection_reason = Column(Text, nullable=True)

    applied_at = Column(DateTime(timezone=True), server_default=func.now())
