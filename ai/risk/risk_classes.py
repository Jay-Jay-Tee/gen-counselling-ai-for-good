"""
Risk class assignment logic
Converts probability scores to Risk Class I, II, III, or IV
Thresholds defined in diseases_config.json for single source of truth
"""

import json
from pathlib import Path

# Module-relative paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DISEASES_PATH = DATA_DIR / "diseases_config.json"


def load_thresholds():
    """Load risk class thresholds from config"""
    try:
        with open(DISEASES_PATH, 'r') as f:
            config = json.load(f)
            return config.get('risk_class_thresholds', {
                'I': {'min': 0.0, 'max': 0.30},
                'II': {'min': 0.30, 'max': 0.55},
                'III': {'min': 0.55, 'max': 0.75},
                'IV': {'min': 0.75, 'max': 1.0}
            })
    except Exception as e:
        print(f"Error loading thresholds: {e}")
        # Fallback to hardcoded
        return {
            'I': {'min': 0.0, 'max': 0.30},
            'II': {'min': 0.30, 'max': 0.55},
            'III': {'min': 0.55, 'max': 0.75},
            'IV': {'min': 0.75, 'max': 1.0}
        }


def get_risk_class(probability: float) -> str:
    """
    Assign risk class based on probability
    
    Args:
        probability: Risk probability (0.0 to 1.0)
    
    Returns:
        Risk class: 'I', 'II', 'III', or 'IV'
    
    Thresholds (loaded from config):
        I:   0.00 - 0.30 (Low)
        II:  0.30 - 0.55 (Moderate)
        III: 0.55 - 0.75 (High)
        IV:  0.75 - 1.00 (Very High)
    """
    
    thresholds = load_thresholds()
    
    if probability < thresholds['II']['min']:
        return 'I'
    elif probability < thresholds['III']['min']:
        return 'II'
    elif probability < thresholds['IV']['min']:
        return 'III'
    else:
        return 'IV'


def get_risk_class_info(risk_class: str) -> dict:
    """
    Get detailed information about a risk class from guidelines.json
    
    Args:
        risk_class: 'I', 'II', 'III', or 'IV'
    
    Returns:
        Dictionary with label, description, color, and guidance
    """
    
    try:
        guidelines_path = DATA_DIR / "guidelines.json"
        with open(guidelines_path, 'r') as f:
            guidelines = json.load(f)
            return guidelines.get('risk_classes', {}).get(risk_class, {})
    except Exception as e:
        print(f"Error loading risk class info: {e}")
        # Fallback
        fallback = {
            'I': {'label': 'Low Risk', 'color': '#22c55e'},
            'II': {'label': 'Moderate Risk', 'color': '#eab308'},
            'III': {'label': 'High Risk', 'color': '#f97316'},
            'IV': {'label': 'Very High Risk', 'color': '#ef4444'}
        }
        return fallback.get(risk_class, fallback['I'])


def get_all_risk_classes() -> dict:
    """
    Return all risk class definitions
    Used for legend/documentation in UI
    """
    return {
        'I': get_risk_class_info('I'),
        'II': get_risk_class_info('II'),
        'III': get_risk_class_info('III'),
        'IV': get_risk_class_info('IV')
    }