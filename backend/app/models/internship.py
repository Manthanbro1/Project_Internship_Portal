from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
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

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    role_title = Column(String, nullable=False)
    role_description = Column(Text, nullable=False)

    required_skills = Column(Text)  # comma-separated (MVP)

    paid = Column(Boolean, default=False)
    stipend_amount = Column(Integer, nullable=True)

    mode = Column(String)  # Online / Offline
    created_at = Column(DateTime(timezone=True), server_default=func.now())
