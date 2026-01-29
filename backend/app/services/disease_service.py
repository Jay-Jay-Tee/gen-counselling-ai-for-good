import json
from pathlib import Path

DISEASE_FILE = Path(__file__).resolve().parents[3] / "ai" / "data" / "diseases_config.json"


def get_disease_list():
    """
    Returns a list of disease objects with 'id' and 'name'.
    Example:
    [
        {"id": "type2_diabetes", "name": "Type-2 Diabetes"},
        {"id": "cad", "name": "Coronary Artery Disease"},
        ...
    ]
    """
    with open(DISEASE_FILE, "r") as f:
        data = json.load(f)
    
    diseases = data.get("diseases", [])
    result = [{"id": d["id"], "name": d["name"]} for d in diseases if "id" in d and "name" in d]
    return result


def get_disease_by_id(disease_id: str):
    """
    Get complete disease information by ID.
    Used for disease detail pages.
    
    Args:
        disease_id: Disease identifier (e.g., "type2_diabetes")
    
    Returns:
        Disease dict or None if not found
    """
    with open(DISEASE_FILE, "r") as f:
        data = json.load(f)
    
    diseases = data.get("diseases", [])
    
    for disease in diseases:
        if disease.get("id") == disease_id:
            return disease
    
    return None