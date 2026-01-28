"""
Main risk prediction engine
Callable by FastAPI: predict_risks(user_data) -> list of disease risk objects
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from .scoring_rules import calculate_family_score, calculate_lifestyle_score, calculate_lab_score
from .risk_classes import get_risk_class
from .explainability import generate_reasons
from ..coaching.consult_logic import get_consult_urgency

# Module-relative paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DISEASES_PATH = DATA_DIR / "diseases_config.json"
GUIDELINES_PATH = DATA_DIR / "guidelines.json"
TESTS_PATH = DATA_DIR / "tests_map.json"


def load_diseases_config():
    """Load disease configuration from JSON"""
    with open(DISEASES_PATH, 'r') as f:
        return json.load(f)['diseases']


def predict_risks(user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Main prediction function
    
    Args:
        user_data: Dictionary containing:
            - patient: {age, gender, height, weight, race, known_issues}
            - lifestyle: {smoking, alcohol, exercise, diet, stress_level, sleep_hours}
            - family: [{role, generation, known_issues}, ...]
            - lab_values: {hba1c, fasting_glucose, ldl, hdl, etc.}
    
    Returns:
        List of disease risk predictions, sorted by probability descending
    """
    
    diseases = load_diseases_config()
    results = []
    
    # Extract patient info for use in scoring
    patient_info = user_data.get('patient', {})
    
    # Build basic_info for compatibility with existing modules
    basic_info = {
        'age': patient_info.get('age', 30),
        'gender': patient_info.get('gender', 'unknown'),
        'bmi': calculate_bmi(patient_info)
    }
    
    # Check lab data completeness for weighting
    lab_values = user_data.get('lab_values', {})
    has_labs = len(lab_values) > 0
    
    for disease in diseases:
        disease_id = disease['id']
        disease_name = disease['name']
        
        # Calculate component scores - FIXED: use 'family' not 'family_history'
        family_score = calculate_family_score(
            disease, 
            user_data.get('family', [])
        )
        
        lifestyle_score = calculate_lifestyle_score(
            disease, 
            user_data.get('lifestyle', {}),
            basic_info
        )
        
        lab_score = calculate_lab_score(
            disease,
            user_data.get('lab_values', {}),
            disease.get('thresholds', {})
        )
        
        # Adjust weights based on data completeness
        if has_labs and disease.get('lab_markers'):
            # Standard weights when labs available
            family_weight = 0.40
            lifestyle_weight = 0.35
            lab_weight = 0.25
        else:
            # Reduce lab weight, redistribute to family/lifestyle when labs missing
            family_weight = 0.50
            lifestyle_weight = 0.40
            lab_weight = 0.10
        
        # Weighted combination for final probability
        base_probability = (
            family_score * family_weight +
            lifestyle_score * lifestyle_weight +
            lab_score * lab_weight
        )
        
        # Apply disease-specific family weight modifier
        disease_family_weight = disease.get('family_weight', 0.30)
        
        # Boost if strong family history
        if family_score > 0.6:
            base_probability = min(1.0, base_probability + (disease_family_weight * 0.15))
        
        # Boost if labs very abnormal
        if lab_score > 0.7:
            base_probability = min(1.0, base_probability + 0.12)
        
        # Gender-specific adjustment for PCOS
        if disease_id == 'pcos' and basic_info.get('gender') not in ['F', 'female', 'Female']:
            base_probability = 0.0
        
        # Age adjustments for certain diseases
        age = basic_info.get('age', 30)
        if disease_id in ['type2_diabetes', 'cad', 'hypertension'] and age > 45:
            base_probability = min(1.0, base_probability + 0.08)
        
        # Cap probability - allow 0.0 for truly low risk, max at 0.99
        probability = min(0.99, max(0.0, base_probability))
        
        # Determine risk class
        risk_class = get_risk_class(probability)
        
        # Generate explanations - pass basic_info for compatibility
        user_data_with_basic = {
            **user_data,
            'basic_info': basic_info
        }
        
        reasons = generate_reasons(
            disease,
            user_data_with_basic,
            family_score,
            lifestyle_score,
            lab_score
        )
        
        # Get prevention recommendations
        prevention = get_prevention_for_disease(disease_id, risk_class)
        
        # Get recommended tests (both simple and detailed)
        tests_simple, tests_detail = get_tests_for_disease(disease_id, risk_class)
        
        # Determine consult urgency using dedicated module
        consult_info = get_consult_urgency(disease_id, risk_class, probability, user_data_with_basic)
        
        results.append({
            'disease_name': disease_name,
            'disease_id': disease_id,
            'probability': round(probability, 2),
            'risk_class': risk_class,
            'reasons': reasons,
            'prevention': prevention,
            'recommended_tests': tests_simple,  # Simple list for FE
            'recommended_tests_detail': tests_detail,  # Full objects
            'consult': consult_info['level'],  # Simple: "urgent", "soon", "routine", "none"
            'consult_detail': consult_info  # Full consultation guidance
        })
    
    # Sort by probability descending
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    return results


def calculate_bmi(patient_info: Dict) -> float:
    """Calculate BMI from patient height and weight"""
    try:
        weight = patient_info.get('weight', 70)
        height = patient_info.get('height', 170)
        
        if height > 0:
            height_m = height / 100  # Convert cm to meters
            bmi = weight / (height_m ** 2)
            return round(bmi, 1)
        return 22.0  # Default
    except:
        return 22.0


def get_prevention_for_disease(disease_id: str, risk_class: str) -> List[str]:
    """Get prevention recommendations based on disease and risk class"""
    try:
        with open(GUIDELINES_PATH, 'r') as f:
            guidelines = json.load(f)
        
        # Get risk class general prevention
        general_prevention = guidelines['risk_classes'].get(risk_class, {}).get('prevention', [])
        
        # Get disease-specific prevention
        disease_prevention = guidelines.get('disease_specific_prevention', {}).get(disease_id, {})
        
        combined = []
        
        # Add top items from disease-specific categories
        if 'diet' in disease_prevention:
            combined.extend(disease_prevention['diet'][:2])
        if 'exercise' in disease_prevention:
            combined.extend(disease_prevention['exercise'][:1])
        if 'lifestyle' in disease_prevention:
            combined.extend(disease_prevention['lifestyle'][:2])
        
        # Add general prevention if high risk
        if risk_class in ['III', 'IV']:
            combined.extend(general_prevention[:2])
        
        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for item in combined:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        
        return deduped[:5]  # Return top 5 recommendations
    
    except Exception as e:
        print(f"Error loading prevention guidelines: {e}")
        return ["Maintain healthy lifestyle", "Regular health checkups"]


def get_tests_for_disease(disease_id: str, risk_class: str) -> tuple:
    """
    Get recommended screening tests for a disease
    Returns: (simple_list, detailed_list)
    """
    try:
        with open(TESTS_PATH, 'r') as f:
            tests_data = json.load(f)
        
        disease_tests = tests_data.get('disease_tests', {}).get(disease_id, [])
        
        # Return simplified test list for FE + full details
        simple = [test['name'] for test in disease_tests[:4]]  # Top 4 tests
        detail = disease_tests[:4]
        
        return simple, detail
    
    except Exception as e:
        print(f"Error loading tests: {e}")
        return ["Consult doctor for appropriate screening"], []