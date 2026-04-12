from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.dependencies import company_only, get_db, student_only
from ..models.project import Project
from ..models.project_skill import ProjectSkill
from ..models.skill import Skill
from ..schemas.project import ProjectCreate, ProjectResponse
from ..services.recommendation import recommend_projects_for_internship

router = APIRouter(prefix="/student", tags=["Students"])


@router.post("/projects", response_model=ProjectResponse)
def add_project(
    data: ProjectCreate,
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    project = Project(
        student_id=user.id,
        title=data.title,
        description=data.description,
        members_count=data.members_count,
        student_role=data.student_role,
        difficulty=data.difficulty,
        status=data.status,
        outcome=data.outcome,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    for skill_name in data.skills:
        normalized_name = skill_name.strip()
        if not normalized_name:
            continue

        skill = db.query(Skill).filter(Skill.name.ilike(normalized_name)).first()
        if not skill:
            skill = Skill(name=normalized_name, is_custom=True)
            db.add(skill)
            db.commit()
            db.refresh(skill)

        try:
            db.add(ProjectSkill(project_id=project.id, skill_id=skill.id))
            db.commit()
        except IntegrityError:
            db.rollback()

    return project


@router.get("/projects", response_model=list[ProjectResponse])
def list_projects(
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    return db.query(Project).filter(Project.student_id == user.id).all()


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id, Project.student_id == user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.get("/projects/recommended/{internship_id}")
def recommended_projects(
    internship_id: int,
    user=Depends(company_only),
    db: Session = Depends(get_db),
):
    return recommend_projects_for_internship(internship_id, db)
