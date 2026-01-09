from pydantic import BaseModel
from typing import Optional

class StudentProfileBase(BaseModel):
    department: Optional[str] = None
    about_me: Optional[str] = None
    github_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    profile_photo: Optional[str] = None
    banner_image: Optional[str] = None


class StudentProfileUpdate(StudentProfileBase):
    pass


class StudentProfileResponse(StudentProfileBase):
    user_id: int

    class Config:
        from_attributes = True
