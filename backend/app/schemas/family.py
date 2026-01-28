from pydantic import BaseModel
from typing import List, Optional

class FamilyMember(BaseModel):
    role: str
    generation: int
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    race: Optional[str] = None
    known_issues: List[str]