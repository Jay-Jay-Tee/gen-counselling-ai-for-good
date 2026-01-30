import tempfile
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
import easyocr
import re
from app.schemas.lab_values import LabValues

# Initialize EasyOCR reader once (expensive operation)
reader = None

def get_reader():
    """Lazy load the OCR reader"""
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'])
    return reader

# -------------------- RULES --------------------

LAB_DEFINITIONS = {
    "hba1c": {
        "labels": [r'hb[a-z]*c', r'a1c', r'glycated'],
        "min_digits": 2
    },
    "fasting_glucose": {
        "labels": [r'fasting.*glucose', r'fbg', r'fbs'],
        "min_digits": 2
    },
    "random_glucose": {
        "labels": [r'random.*glucose', r'rbs'],
        "min_digits": 2
    },
    "ldl": {
        "labels": [r'ldl'],
        "min_digits": 2
    },
    "hdl": {
        "labels": [r'hdl'],
        "min_digits": 2
    },
    "triglycerides": {
        "labels": [r'triglycerides', r'trig'],
        "min_digits": 2
    },
    "total_cholesterol": {
        "labels": [r'total.*cholesterol', r'cholesterol.*total'],
        "min_digits": 2
    },
    "hemoglobin": {
        "labels": [r'hemoglobin', r'hb[^a-z]', r'\bhb\b'],
        "min_digits": 2
    },
    "rbc": {
        "labels": [r'rbc', r'red.*blood.*cell'],
        "min_digits": 1
    },
    "tsh": {
        "labels": [r'tsh', r'thyroid.*stimulating'],
        "min_digits": 1
    },
    "t4": {
        "labels": [r't4', r'thyroxine'],
        "min_digits": 1
    },
    "t3": {
        "labels": [r't3', r'triiodothyronine'],
        "min_digits": 1
    }
}

# -------------------- EXTRACTION --------------------

def preprocess(text: str) -> str:
    """Preprocess text for easier parsing"""
    return text.lower()

def extract_single_value(text: str, label_patterns: list[str], *, min_digits=1) -> Optional[float]:
    """Extract a single numeric value associated with a label"""
    for label in label_patterns:
        # Look for label followed by value (with some characters in between)
        pattern = rf'{label}[^0-9]{{0,30}}([\d]+\.?\d*)'
        match = re.search(pattern, text)
        if match:
            value = match.group(1)
            if len(value.replace('.', '')) >= min_digits:
                try:
                    return float(value)
                except ValueError:
                    continue
    return None

def extract_blood_pressure(text: str) -> tuple[Optional[float], Optional[float]]:
    """Extract blood pressure values (systolic/diastolic)"""
    match = re.search(
        r'(blood pressure|bp)[^0-9]*([1-9]\d{1,2})\s*/\s*([1-9]\d{1,2})',
        text
    )
    if match:
        return float(match.group(2)), float(match.group(3))
    return None, None

def parse_lab_values(text: str) -> dict:
    """Parse lab values from extracted text"""
    results = {}

    for lab, config in LAB_DEFINITIONS.items():
        value = extract_single_value(
            text,
            config["labels"],
            min_digits=config["min_digits"]
        )
        if value is not None:
            results[lab] = value

    systolic, diastolic = extract_blood_pressure(text)
    if systolic is not None:
        results["systolic_bp"] = systolic
    if diastolic is not None:
        results["diastolic_bp"] = diastolic

    return results

# -------------------- OCR PROCESSING --------------------

def extract_raw_text(image_path: str) -> str:
    """Extract text from image using EasyOCR"""
    ocr_reader = get_reader()
    result = ocr_reader.readtext(image_path)
    text = " ".join([item[1] for item in result])
    return text

async def process_image_file(file: UploadFile) -> dict:
    """Process uploaded image file and extract lab values"""
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name
    
    try:
        # Extract text using OCR
        raw_text = extract_raw_text(tmp_path)
        
        # Preprocess and parse
        processed_text = preprocess(raw_text)
        parsed_values = parse_lab_values(processed_text)
        
        return parsed_values
    finally:
        # Clean up temporary file
        Path(tmp_path).unlink(missing_ok=True)

# -------------------- SERVICE FUNCTION --------------------

async def extract_lab_values_from_file(file: UploadFile) -> LabValues:
    """
    Main service function to extract lab values from uploaded file
    Returns LabValues schema with extracted values
    """
    try:
        # Process the file and extract values
        extracted_values = await process_image_file(file)
        
        # Create LabValues object with extracted values
        # If a value is not found, it will be None
        lab_values = LabValues(
            hba1c=extracted_values.get('hba1c'),
            fasting_glucose=extracted_values.get('fasting_glucose'),
            random_glucose=extracted_values.get('random_glucose'),
            ldl=extracted_values.get('ldl'),
            hdl=extracted_values.get('hdl'),
            triglycerides=extracted_values.get('triglycerides'),
            total_cholesterol=extracted_values.get('total_cholesterol'),
            systolic_bp=extracted_values.get('systolic_bp'),
            diastolic_bp=extracted_values.get('diastolic_bp'),
            hemoglobin=extracted_values.get('hemoglobin'),
            rbc=extracted_values.get('rbc'),
            tsh=extracted_values.get('tsh'),
            t4=extracted_values.get('t4'),
            t3=extracted_values.get('t3')
        )
        
        return lab_values
        
    except Exception as e:
        # Log the error and return empty LabValues
        print(f"Error processing OCR: {str(e)}")
        # Return with None values if extraction fails
        return LabValues()

