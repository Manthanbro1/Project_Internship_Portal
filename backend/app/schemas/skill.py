# backend/app/schemas/skill.py
from pydantic import BaseModel

class SkillResponse(BaseModel):
    id: int
    name: str
    is_custom: bool

    class Config:
        from_attributes = True
