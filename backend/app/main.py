# uvicorn backend.app.main:app --reload
from fastapi import FastAPI
from .database.session import engine
from .database.base import Base
# 🔥 IMPORTANT: import all models so SQLAlchemy knows them
from .models.user import User
from .models.student_profiile import StudentProfile
from .models.company_profile import CompanyProfile
from .models.project import Project
from .models.skill import Skill
from .models.project_skill import Project_Skill
from .models.internship import Internship
from .models.application import Application
from .models.application_project import ApplicationProject

app = FastAPI(title="Project-Centric Internship Platform")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Backend running"}
