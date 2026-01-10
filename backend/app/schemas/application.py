# backend/app/schemas/application.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    internship_id: int
    project_ids: List[int]


class ApplicationResponse(BaseModel):
    id: int
    status: str
    rejection_reason: Optional[str] = None
    applied_at: datetime

    class Config:
        from_attributes = True
