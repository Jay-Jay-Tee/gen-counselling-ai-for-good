from pydantic import Field
from app.schemas.profile import PatientProfile


class FamilyMember(PatientProfile):
    role: str
    generation: int = Field(..., ge=1)
