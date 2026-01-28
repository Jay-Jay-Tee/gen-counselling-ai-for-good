from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.schemas.profile import PatientProfile
from app.schemas.family import FamilyMember
from app.schemas.lab_values import LabValues
from app.schemas.lifestyle import Lifestyle


class RiskRequest(BaseModel):
    """Request payload for risk prediction"""
    patient: PatientProfile
    lifestyle: Lifestyle
    family: List[FamilyMember]
    lab_values: Optional[LabValues] = None


class ConsultDetail(BaseModel):
    """Detailed consultation guidance"""
    level: str
    timeframe: str
    message: str
    specialist: Dict[str, Any]
    what_to_discuss: List[str]
    preparation: List[str]


class DiseaseRiskResult(BaseModel):
    """Individual disease risk result - matches AI output exactly"""
    disease_name: str
    disease_id: str
    probability: float = Field(..., ge=0.0, le=1.0)
    risk_class: str  # "I", "II", "III", or "IV"
    reasons: List[str]
    prevention: List[str]
    recommended_tests: List[str]
    recommended_tests_detail: Optional[List[Dict[str, Any]]] = []
    consult: str  # "none", "routine", "soon", "urgent"
    consult_detail: ConsultDetail


class RiskResponse(BaseModel):
    """Response from prediction endpoint"""
    success: bool = True
    results: List[DiseaseRiskResult]