from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DiseaseOption(BaseModel):
    """
    Simplified disease model for frontend selection lists.
    Used in dropdowns, checkboxes, etc.
    """
    id: str = Field(..., description="Unique disease identifier (e.g., 'type2_diabetes')")
    name: str = Field(..., description="Human-readable disease name (e.g., 'Type-2 Diabetes')")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "type2_diabetes",
                "name": "Type-2 Diabetes"
            }
        }


class DiseaseThresholds(BaseModel):
    """Lab value thresholds for disease risk assessment"""
    # Dynamic thresholds - varies by disease
    # Examples: hba1c_prediabetic, ldl_high, systolic_elevated, etc.
    pass  # This is a flexible dict in practice

    class Config:
        extra = "allow"  # Allow any additional fields


class DiseaseDetail(BaseModel):
    """
    Complete disease information including clinical details.
    Used for disease detail pages and risk calculation.
    """
    id: str = Field(..., description="Unique disease identifier")
    name: str = Field(..., description="Disease name")
    description: str = Field(..., description="Clinical description of the disease")
    
    # Risk calculation weights
    family_weight: float = Field(..., ge=0.0, le=1.0, description="Weight of family history in risk calculation")
    
    # Associated factors
    lifestyle_factors: List[str] = Field(default_factory=list, description="Lifestyle risk factors")
    lab_markers: List[str] = Field(default_factory=list, description="Relevant lab test markers")
    
    # Thresholds for lab values
    thresholds: Dict[str, Any] = Field(default_factory=dict, description="Lab value thresholds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "type2_diabetes",
                "name": "Type-2 Diabetes",
                "description": "A chronic condition where the body becomes resistant to insulin...",
                "family_weight": 0.35,
                "lifestyle_factors": ["high_sugar", "sedentary", "obesity", "stress"],
                "lab_markers": ["hba1c", "fasting_glucose", "random_glucose"],
                "thresholds": {
                    "hba1c_prediabetic": 5.7,
                    "hba1c_diabetic": 6.5,
                    "fasting_glucose_prediabetic": 100,
                    "fasting_glucose_diabetic": 126
                }
            }
        }


class DiseaseListResponse(BaseModel):
    """Response model for disease list endpoint"""
    diseases: List[DiseaseOption]

    class Config:
        json_schema_extra = {
            "example": {
                "diseases": [
                    {"id": "type2_diabetes", "name": "Type-2 Diabetes"},
                    {"id": "cad", "name": "Coronary Artery Disease"},
                    {"id": "hypertension", "name": "Hypertension"}
                ]
            }
        }


class DiseaseCategory(BaseModel):
    """Disease category for grouping related conditions"""
    category: str = Field(..., description="Category name (e.g., 'Cardiovascular', 'Metabolic')")
    diseases: List[DiseaseOption]

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Cardiovascular",
                "diseases": [
                    {"id": "cad", "name": "Coronary Artery Disease"},
                    {"id": "hypertension", "name": "Hypertension"}
                ]
            }
        }


class DiseaseCategoriesResponse(BaseModel):
    """Response model for categorized disease list"""
    categories: List[DiseaseCategory]


# Export all models
__all__ = [
    "DiseaseOption",
    "DiseaseThresholds",
    "DiseaseDetail",
    "DiseaseListResponse",
    "DiseaseCategory",
    "DiseaseCategoriesResponse"
]