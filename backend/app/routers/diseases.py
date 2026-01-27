from fastapi import APIRouter
from typing import List
from app.services.disease_service import get_disease_list
from app.schemas.diseases import DiseaseOption

router = APIRouter(prefix="/disease-info", tags=["Diseases"])

@router.get("/list", response_model=List[DiseaseOption])
def disease_list():
    """
    Returns a list of disease IDs and names for frontend checkboxes.
    """
    return get_disease_list()