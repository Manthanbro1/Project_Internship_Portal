from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.base import Base
from .database.session import engine
from .models.application import Application
from .models.application_project import ApplicationProject
from .models.company_profile import CompanyProfile
from .models.internship import Internship
from .models.project import Project
from .models.project_skill import ProjectSkill
from .models.skill import Skill
from .models.student_profile import StudentProfile
from .models.user import User
from .routers import applications, auth, company, internships, projects, student

app = FastAPI(title="Project-Centric Internship Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
