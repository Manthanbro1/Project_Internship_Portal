from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    internship_id: int
    project_ids: List[int]


class ApplicationStatusUpdate(BaseModel):
    status: Literal["Shortlisted", "Selected", "Rejected"]
    rejection_reason: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    internship_id: int
    status: Literal["Applied", "Shortlisted", "Selected", "Rejected"]
    rejection_reason: Optional[str] = None
    applied_at: datetime

    class Config:
        from_attributes = True
