from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from app.schemas.profile import PatientProfile
from app.schemas.family import FamilyMember

class RiskLevel(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"

class Recommendation(str, Enum):
    none = "none"
    consult_soon = "consult_soon"
    consult_urgent = "consult_urgent"

class DiseaseRisk(BaseModel):
    disease: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: RiskLevel
    factors: List[str]
    recommendation: Recommendation

class RiskResponse(BaseModel):
    patient_name: str
    results: List[DiseaseRisk]

class RiskRequest(BaseModel):
    patient: PatientProfile
    family: List[FamilyMember]

