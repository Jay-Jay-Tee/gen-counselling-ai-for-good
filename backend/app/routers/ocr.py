from fastapi import APIRouter, UploadFile, File
from app.schemas.lab_values import LabValues
from app.services.ocr_service import extract_lab_values_from_file

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/", response_model=LabValues)
async def extract_lab_values(file: UploadFile = File(...)):
    return extract_lab_values_from_file(file)
