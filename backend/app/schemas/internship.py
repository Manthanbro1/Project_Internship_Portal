# backend/app/schemas/internship.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InternshipCreate(BaseModel):
    role_title: str
    role_description: str
    required_skills: str
    paid: bool
    stipend_amount: Optional[int] = None
    mode: str


class InternshipResponse(BaseModel):
    id: int
    role_title: str
    role_description: str
    paid: bool
    mode: str
    created_at: datetime

    class Config:
        from_attributes = True
