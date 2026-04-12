from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    description: str
    members_count: Optional[int] = None
    student_role: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    status: Literal["Idea", "Ongoing", "Completed"]
    outcome: Optional[str] = None
    skills: List[str]


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    student_role: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    status: Literal["Idea", "Ongoing", "Completed"]
    created_at: datetime

    class Config:
        from_attributes = True
