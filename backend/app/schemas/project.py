# backend/app/schemas/project.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: str
    members_count: Optional[int] = None
    student_role: str
    difficulty: str
    status: str
    outcome: Optional[str] = None
    skills: List[str]   # hybrid model


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    student_role: str
    difficulty: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
