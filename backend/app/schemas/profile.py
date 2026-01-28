from pydantic import BaseModel, Field
from typing import List, Optional

class PatientProfile(BaseModel):
    age: int = Field(..., ge=15, le=100)
    gender: str = Field(..., pattern="^(M|F|Other)$")
    weight: float
    height: float
    race: Optional[str] = None
    known_issues: Optional[List[str]] = []
