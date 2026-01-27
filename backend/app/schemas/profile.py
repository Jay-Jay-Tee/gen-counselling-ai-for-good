from pydantic import BaseModel, Field
from typing import List


class PatientProfile(BaseModel):
    age: int = Field(..., gt=0, lt=150)
    gender: str
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    race: str
    vision: float = Field(..., gt=0)
    sugar_level: float = Field(..., ge=0)
    RBC: float = Field(..., gt=0)
    known_issues: List[str]
