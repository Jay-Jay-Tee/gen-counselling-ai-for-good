import json
from pathlib import Path

DISEASE_FILE = Path(__file__).parent.parent.parent / "ai" / "data" / "diseases_config.json"

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
