from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from ..database.base import Base


class ApplicationProject(Base):
    __tablename__ = "application_projects"
    __table_args__ = (
        UniqueConstraint("application_id", "project_id", name="uq_application_projects_pair"),
    )

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
