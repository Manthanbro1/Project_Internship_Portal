from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class InternshipCreate(BaseModel):
    role_title: str
    role_description: str
    required_skills: str
    paid: bool
    stipend_amount: Optional[int] = None
    mode: Literal["Online", "Offline"]


class InternshipResponse(BaseModel):
    id: int
    role_title: str
    role_description: str
    paid: bool
    mode: Literal["Online", "Offline"]
    created_at: datetime

    class Config:
        from_attributes = True
