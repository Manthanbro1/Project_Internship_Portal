# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # student | company
    created_at = Column(DateTime(timezone=True), server_default=func.now())
