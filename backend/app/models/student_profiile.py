from sqlalchemy import Column, Integer, String, Text, ForeignKey

# Replace the single relative import with a tolerant import:
try:
    # normal package import (when used as part of app)
    from ..database.base import Base
except (ImportError, ValueError):
    # fallback when running the file directly (no parent package)
    import os
    import sys
    # add backend folder to sys.path so absolute package import works
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)
    from app.database.base import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    department = Column(String)
    about_me = Column(Text)

    profile_photo = Column(String)
    banner_image = Column(String)

    github_link = Column(String)
    linkedin_link = Column(String)
