# backend/app/routers/student.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.dependencies import student_only, get_db
from ..models.user import User
from ..models.student_profile import StudentProfile
from ..schemas.student_profile import (
    StudentProfileResponse,
    StudentProfileUpdate
)

router = APIRouter(prefix="/student", tags=["Students"])

@router.get("/profile", response_model=StudentProfileResponse)
def get_profile(
    user: User = Depends(student_only),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == user.id
    ).first()

    if not profile:
        profile = StudentProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile

@router.put("/profile", response_model=StudentProfileResponse)
def update_profile(
    data: StudentProfileUpdate,
    user: User = Depends(student_only),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == user.id
    ).first()

    if not profile:
        profile = StudentProfile(user_id=user.id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile
