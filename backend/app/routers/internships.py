from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.dependencies import company_only, get_db, student_only
from ..models.internship import Internship
from ..schemas.internship import InternshipCreate, InternshipResponse
from ..services.recommendation import recommend_internships_for_student

router = APIRouter(tags=["Internships"])


@router.post("/company/internships", response_model=InternshipResponse)
def post_internship(
    data: InternshipCreate,
    user=Depends(company_only),
    db: Session = Depends(get_db),
):
    internship = Internship(
        company_id=user.id,
        role_title=data.role_title,
        role_description=data.role_description,
        required_skills=data.required_skills,
        paid=data.paid,
        stipend_amount=data.stipend_amount,
        mode=data.mode,
    )

    db.add(internship)
    db.commit()
    db.refresh(internship)
    return internship


@router.get("/company/internships", response_model=list[InternshipResponse])
def list_company_internships(
    user=Depends(company_only),
    db: Session = Depends(get_db),
):
    return db.query(Internship).filter(Internship.company_id == user.id).all()


@router.get("/student/internships", response_model=list[InternshipResponse])
def list_student_internships(
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    return db.query(Internship).all()


@router.get("/student/internships/recommended")
@router.get("/company/internships/recommended", deprecated=True)
def recommended_internships(
    user=Depends(student_only),
    db: Session = Depends(get_db),
):
    return recommend_internships_for_student(user.id, db)
