from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.services.disease_service import get_disease_list, get_disease_by_id
from app.schemas.diseases import DiseaseOption

router = APIRouter(prefix="/disease-info", tags=["Diseases"])

@router.get("", response_model=Dict[str, List[DiseaseOption]])
def disease_info():
    """
    Returns disease list for frontend checkboxes.
    Matches frontend expectation: /disease-info
    """
    diseases = get_disease_list()
    return {"diseases": diseases}


@router.get("/{disease_id}")
def get_disease_detail(disease_id: str):
    """
    Get detailed information about a specific disease.
    Used by DiseaseDetail.jsx
    """
    disease = get_disease_by_id(disease_id)
    
    if not disease:
        raise HTTPException(status_code=404, detail=f"Disease '{disease_id}' not found")
    
    return disease