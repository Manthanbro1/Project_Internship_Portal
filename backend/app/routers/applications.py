# backend/app/routers/applications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.dependencies import student_only, company_only, get_db
from ..models.application import Application
from ..models.application_project import ApplicationProject
from ..models.project import Project
from ..models.internship import Internship
from ..schemas.application import ApplicationCreate, ApplicationResponse

router = APIRouter(tags=["Applications"])
@router.post("/applications", response_model=ApplicationResponse)
def apply_to_internship(
    data: ApplicationCreate,
    user = Depends(student_only),
    db: Session = Depends(get_db)
):
    if not (1 <= len(data.project_ids) <= 3):
        raise HTTPException(
            status_code=400,
            detail="Attach between 1 and 3 projects"
        )

    internship = db.query(Internship).filter(
        Internship.id == data.internship_id
    ).first()

    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    projects = db.query(Project).filter(
        Project.id.in_(data.project_ids),
        Project.student_id == user.id
    ).all()

    if len(projects) != len(data.project_ids):
        raise HTTPException(
            status_code=403,
            detail="Invalid project selection"
        )

    application = Application(
        student_id=user.id,
        internship_id=data.internship_id,
        status="Applied"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    for project in projects:
        db.add(ApplicationProject(
            application_id=application.id,
            project_id=project.id
        ))

    db.commit()

    return application
@router.get("/student/applications", response_model=list[ApplicationResponse])
def student_applications(
    user = Depends(student_only),
    db: Session = Depends(get_db)
):
    return db.query(Application).filter(
        Application.student_id == user.id
    ).all()
@router.get("/company/applications")
def company_applications(
    user = Depends(company_only),
    db: Session = Depends(get_db)
):
    return (
        db.query(Application)
        .join(Internship)
        .filter(Internship.company_id == user.id)
        .all()
    )
@router.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    status: str,
    rejection_reason: str | None = None,
    user = Depends(company_only),
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .join(Internship)
        .filter(
            Application.id == application_id,
            Internship.company_id == user.id
        )
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if status == "Rejected" and not rejection_reason:
        raise HTTPException(
            status_code=400,
            detail="Rejection reason required"
        )

    application.status = status
    application.rejection_reason = rejection_reason

    db.commit()
    db.refresh(application)

    return {"message": "Status updated"}
