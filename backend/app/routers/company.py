from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.dependencies import company_only, get_db
from ..models.company_profile import CompanyProfile
from ..models.user import User
from ..schemas.company_profile import (
    CompanyProfileResponse,
    CompanyProfileUpdate
)

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("/profile", response_model=CompanyProfileResponse)
def get_profile(
    user: User = Depends(company_only),
    db: Session = Depends(get_db)
):
    profile = db.query(CompanyProfile).filter(
        CompanyProfile.user_id == user.id
    ).first()

    if not profile:
        profile = CompanyProfile(user_id=user.id, sector="")
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile

@router.put("/profile", response_model=CompanyProfileResponse)
def update_profile(
    data: CompanyProfileUpdate,
    user: User = Depends(company_only),
    db: Session = Depends(get_db)
):
    profile = db.query(CompanyProfile).filter(
        CompanyProfile.user_id == user.id
    ).first()

    if not profile:
        profile = CompanyProfile(user_id=user.id)

    for field, value in data.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile
