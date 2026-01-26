"""
Main risk prediction engine
Callable by FastAPI: predict_risks(user_data) -> list of disease risk objects
"""

import json
from typing import Dict, List, Any
from .scoring_rules import calculate_family_score, calculate_lifestyle_score, calculate_lab_score
from .risk_classes import get_risk_class
from .explainability import generate_reasons


def load_diseases_config():
    """Load disease configuration from JSON"""
    with open('data/diseases_config.json', 'r') as f:
        return json.load(f)['diseases']


def predict_risks(user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Main prediction function
    
    Args:
        user_data: Dictionary containing:
            - basic_info: {age, gender, height, weight, bmi}
            - lifestyle: {smoking, alcohol, exercise, diet, stress_level, sleep_hours}
            - family_history: {generation_1: {}, generation_2: {}}
            - lab_values: {hba1c, fasting_glucose, ldl, hdl, etc.}
    
    Returns:
        List of disease risk predictions, sorted by probability descending
    """
    
    diseases = load_diseases_config()
    results = []
    
    for disease in diseases:
        disease_id = disease['id']
        disease_name = disease['name']
        
        
        family_score = calculate_family_score(
            disease, 
            user_data.get('family_history', {})
        )
        
        lifestyle_score = calculate_lifestyle_score(
            disease, 
            user_data.get('lifestyle', {}),
            user_data.get('basic_info', {})
        )
        
        lab_score = calculate_lab_score(
            disease,
            user_data.get('lab_values', {}),
            disease.get('thresholds', {})
        )
        
        
        
        base_probability = (
            family_score * 0.40 +
            lifestyle_score * 0.35 +
            lab_score * 0.25
        )
        
        
        family_weight = disease.get('family_weight', 0.30)
        
        
        if family_score > 0.6:
            base_probability = min(1.0, base_probability + (family_weight * 0.15))
        
        
        if lab_score > 0.7:
            base_probability = min(1.0, base_probability + 0.12)
        
        
        if disease_id == 'pcos' and user_data.get('basic_info', {}).get('gender') != 'female':
            base_probability = 0.0
        
        
        age = user_data.get('basic_info', {}).get('age', 30)
        if disease_id in ['type2_diabetes', 'cad', 'hypertension'] and age > 45:
            base_probability = min(1.0, base_probability + 0.08)
        
        
        probability = min(0.95, max(0.05, base_probability))
        
        
        risk_class = get_risk_class(probability)
        
        
        reasons = generate_reasons(
            disease,
            user_data,
            family_score,
            lifestyle_score,
            lab_score
        )
        
        
        prevention = get_prevention_for_disease(disease_id, risk_class)
        
        
        tests = get_tests_for_disease(disease_id)
        
        
        consult = get_consult_urgency(risk_class, probability)
        
        results.append({
            'disease_name': disease_name,
            'disease_id': disease_id,
            'probability': round(probability, 2),
            'risk_class': risk_class,
            'reasons': reasons,
            'prevention': prevention,
            'recommended_tests': tests,
            'consult': consult
        })
    
    
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    return results


def get_prevention_for_disease(disease_id: str, risk_class: str) -> List[str]:
    """Get prevention recommendations based on disease and risk class"""
    try:
        with open('data/guidelines.json', 'r') as f:
            guidelines = json.load(f)
        
        
        general_prevention = guidelines['risk_classes'].get(risk_class, {}).get('prevention', [])
        
        
        disease_prevention = guidelines.get('disease_specific_prevention', {}).get(disease_id, {})
        
        combined = []
        
        
        if 'diet' in disease_prevention:
            combined.extend(disease_prevention['diet'][:2])
        if 'exercise' in disease_prevention:
            combined.extend(disease_prevention['exercise'][:1])
        if 'lifestyle' in disease_prevention:
            combined.extend(disease_prevention['lifestyle'][:2])
        
        
        if risk_class in ['III', 'IV']:
            combined.extend(general_prevention[:2])
        
        return combined[:5]  
    
    except Exception as e:
        print(f"Error loading prevention guidelines: {e}")
        return ["Maintain healthy lifestyle", "Regular health checkups"]


def get_tests_for_disease(disease_id: str) -> List[str]:
    """Get recommended screening tests for a disease"""
    try:
        with open('data/tests_map.json', 'r') as f:
            tests_data = json.load(f)
        
        disease_tests = tests_data.get('disease_tests', {}).get(disease_id, [])
        
        
        return [test['name'] for test in disease_tests[:4]]  
    
    except Exception as e:
        print(f"Error loading tests: {e}")
        return ["Consult doctor for appropriate screening"]


def get_consult_urgency(risk_class: str, probability: float) -> str:
    """Determine consultation urgency"""
    if risk_class == 'IV' or probability >= 0.75:
        return "Urgent"
    elif risk_class == 'III' or probability >= 0.55:
        return "Soon"
    else:
        return "Routine"