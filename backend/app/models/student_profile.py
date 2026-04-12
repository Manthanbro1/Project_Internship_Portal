from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint

from ..database.base import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_student_profiles_user_id"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    department = Column(String)
    about_me = Column(Text)

    profile_photo = Column(String)
    banner_image = Column(String)

    github_link = Column(String)
    linkedin_link = Column(String)
