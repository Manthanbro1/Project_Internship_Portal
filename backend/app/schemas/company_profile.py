from pydantic import BaseModel
from typing import Optional

class CompanyProfileBase(BaseModel):
    sector: str
    description: Optional[str] = None
    website_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    profile_photo: Optional[str] = None
    banner_image: Optional[str] = None


class CompanyProfileUpdate(CompanyProfileBase):
    pass


class CompanyProfileResponse(CompanyProfileBase):
    user_id: int

    class Config:
        from_attributes = True
