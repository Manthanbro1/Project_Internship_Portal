from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint

from ..database.base import Base


class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_company_profiles_user_id"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sector = Column(String, nullable=False)
    description = Column(Text)

    profile_photo = Column(String)
    banner_image = Column(String)

    website_link = Column(String)
    linkedin_link = Column(String)
