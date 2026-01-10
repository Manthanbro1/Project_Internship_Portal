# backend/app/models/application_project.py
from sqlalchemy import Column, Integer, ForeignKey
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

class ApplicationProject(Base):
    __tablename__ = "application_projects"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
