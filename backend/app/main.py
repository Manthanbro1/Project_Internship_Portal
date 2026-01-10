# uvicorn backend.app.main:app --reload
# backend/app/main.py
from fastapi import FastAPI
from .database.session import engine
from .database.base import Base
# 🔥 IMPORTANT: import all models so SQLAlchemy knows them
from .models.user import User
from .models.student_profile import StudentProfile
from .models.company_profile import CompanyProfile
from .models.project import Project
from .models.skill import Skill
from .models.project_skill import Project_Skill
from .models.internship import Internship
from .models.application import Application
from .models.application_project import ApplicationProject
from .routers import auth
from .routers import student,projects
from .routers import company, internships
from .routers import applications
app = FastAPI(title="Project-Centric Internship Platform")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status": "Backend running"}

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(projects.router)
app.include_router(company.router)
app.include_router(internships.router)
app.include_router(applications.router)
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE3NjgxMzc2ODl9.SpUpd1BHN_Ha4DJ17OFXXQsWPG0_rhalYPDPE9H2WSk