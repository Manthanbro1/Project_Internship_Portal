# backend/app/routers/internships.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services.recommendation import recommend_internships_for_student
from ..core.dependencies import student_only
from ..core.dependencies import company_only, get_db
from ..models.internship import Internship
from ..schemas.internship import InternshipCreate, InternshipResponse

router = APIRouter(prefix="/company", tags=["Internships"])

@router.post("/internships", response_model=InternshipResponse)
def post_internship(
    data: InternshipCreate,
    user = Depends(company_only),
    db: Session = Depends(get_db)
):
    internship = Internship(
        company_id=user.id,
        role_title=data.role_title,
        role_description=data.role_description,
        required_skills=data.required_skills,
        paid=data.paid,
        stipend_amount=data.stipend_amount,
        mode=data.mode
    )

    db.add(internship)
    db.commit()
    db.refresh(internship)

    return internship

@router.get("/internships", response_model=list[InternshipResponse])
def list_internships(
    user = Depends(company_only),
    db: Session = Depends(get_db)
):
    return db.query(Internship).filter(
        Internship.company_id == user.id
    ).all()

@router.get("/internships/recommended")
def recommended_internships(
    user = Depends(student_only),
    db: Session = Depends(get_db)
):
    return recommend_internships_for_student(user.id, db)
