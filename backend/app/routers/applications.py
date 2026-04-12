from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.dependencies import company_only, get_db, student_only
from ..models.application import Application
from ..models.application_project import ApplicationProject
from ..models.internship import Internship
from ..models.project import Project
from ..schemas.application import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate

router = APIRouter(tags=["Applications"])


@router.post("/applications", response_model=ApplicationResponse)
def apply_to_internship(
    data: ApplicationCreate,
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    if not (1 <= len(data.project_ids) <= 3):
        raise HTTPException(status_code=400, detail="Attach between 1 and 3 projects")

    internship = db.query(Internship).filter(Internship.id == data.internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")

    existing_application = (
        db.query(Application)
        .filter(
            Application.student_id == user.id,
            Application.internship_id == data.internship_id,
        )
        .first()
    )
    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied to this internship")

    unique_project_ids = list(dict.fromkeys(data.project_ids))
    projects = (
        db.query(Project)
        .filter(Project.id.in_(unique_project_ids), Project.student_id == user.id)
        .all()
    )
    if len(projects) != len(unique_project_ids):
        raise HTTPException(status_code=403, detail="Invalid project selection")

    application = Application(student_id=user.id, internship_id=data.internship_id, status="Applied")
    db.add(application)
    db.commit()
    db.refresh(application)

    try:
        for project in projects:
            db.add(ApplicationProject(application_id=application.id, project_id=project.id))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate project attachment") from exc

    db.refresh(application)
    return application


@router.get("/student/applications", response_model=list[ApplicationResponse])
def student_applications(
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    return db.query(Application).filter(Application.student_id == user.id).all()


@router.get("/company/applications", response_model=list[ApplicationResponse])
def company_applications(
    user=Depends(company_only),
    db: Session = Depends(get_db),
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
    payload: ApplicationStatusUpdate | None = Body(default=None),
    status: str | None = Query(default=None),
    rejection_reason: str | None = Query(default=None),
    user=Depends(company_only),
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .join(Internship)
        .filter(Application.id == application_id, Internship.company_id == user.id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if payload is not None:
        target_status = payload.status
        target_reason = payload.rejection_reason
    else:
        if status not in {"Shortlisted", "Selected", "Rejected"}:
            raise HTTPException(status_code=400, detail="Invalid status")
        target_status = status
        target_reason = rejection_reason

    if target_status == "Rejected" and not target_reason:
        raise HTTPException(status_code=400, detail="Rejection reason required")
    if target_status != "Rejected":
        target_reason = None

    application.status = target_status
    application.rejection_reason = target_reason

    db.commit()
    db.refresh(application)
    return {"message": "Status updated"}
