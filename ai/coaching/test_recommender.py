"""
Screening test recommender
Suggests appropriate medical tests based on disease risk and user profile
"""

import json
from typing import Dict, List, Any


def load_tests_map():
    """Load tests mapping from JSON"""
    try:
        with open('data/tests_map.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tests map: {e}")
        return {}


def get_recommended_tests(
    disease_id: str,
    risk_class: str,
    user_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Get recommended screening tests for a disease
    
    Args:
        disease_id: Disease identifier
        risk_class: 'I', 'II', 'III', or 'IV'
        user_data: User profile data
    
    Returns:
        List of test dictionaries with name, frequency, why, normal_range
    """
    
    tests_map = load_tests_map()
    disease_tests = tests_map.get('disease_tests', {}).get(disease_id, [])
    
    if not disease_tests:
        return []
    
    # Filter and prioritize based on risk class
    recommended = []
    
    for test in disease_tests:
        priority = calculate_test_priority(test, disease_id, risk_class, user_data)
        
        if priority > 0:
            test_info = {
                'name': test['name'],
                'frequency': adjust_frequency(test['frequency'], risk_class),
                'why': test['why'],
                'normal_range': test.get('normal_range', 'Consult report'),
                'priority': priority
            }
            recommended.append(test_info)
    
    # Sort by priority (descending)
    recommended.sort(key=lambda x: x['priority'], reverse=True)
    
    # Return top tests based on risk class
    max_tests = {
        'I': 2,
        'II': 3,
        'III': 5,
        'IV': 6
    }
    
    return recommended[:max_tests.get(risk_class, 3)]


def calculate_test_priority(
    test: Dict,
    disease_id: str,
    risk_class: str,
    user_data: Dict
) -> int:
    """
    Calculate priority score for a test
    Higher score = more important
    """
    
    priority = 5  # Base priority
    test_name = test['name'].lower()
    
    # Risk class multiplier
    risk_multipliers = {
        'I': 0.5,
        'II': 1.0,
        'III': 1.5,
        'IV': 2.0
    }
    priority *= risk_multipliers.get(risk_class, 1.0)
    
    # Disease-specific priorities
    if disease_id == 'type2_diabetes':
        if 'hba1c' in test_name or 'glucose' in test_name:
            priority += 3
    
    elif disease_id == 'cad':
        if 'lipid' in test_name or 'cholesterol' in test_name:
            priority += 3
        if 'ecg' in test_name or 'stress' in test_name:
            priority += 2
    
    elif disease_id == 'hypertension':
        if 'blood pressure' in test_name:
            priority += 4
        if 'kidney' in test_name or 'creatinine' in test_name:
            priority += 2
    
    elif disease_id == 'breast_ovarian_cancer':
        if 'brca' in test_name or 'genetic' in test_name:
            priority += 4
        if 'mammogram' in test_name or 'mri' in test_name:
            priority += 3
    
    elif disease_id == 'familial_hypercholesterolemia':
        if 'genetic' in test_name:
            priority += 4
        if 'lipid' in test_name or 'apob' in test_name:
            priority += 3
    
    # Age-based adjustments
    age = user_data.get('basic_info', {}).get('age', 30)
    
    if age > 40:
        if 'screening' in test_name or 'baseline' in test_name:
            priority += 1
    
    if age > 50:
        if any(word in test_name for word in ['calcium score', 'mammogram', 'colonoscopy']):
            priority += 2
    
    # Gender-specific
    gender = user_data.get('basic_info', {}).get('gender', 'unknown')
    
    if gender == 'female':
        if any(word in test_name for word in ['breast', 'mammogram', 'ovarian', 'ca-125']):
            priority += 2
    
    # Family history boost
    family_history = user_data.get('family_history', {})
    if has_family_history_for_disease(family_history, disease_id):
        if 'genetic' in test_name:
            priority += 3
    
    return int(priority)


def adjust_frequency(base_frequency: str, risk_class: str) -> str:
    """
    Adjust test frequency based on risk class
    """
    
    frequency_adjustments = {
        'I': {
            'Every 3-6 months': 'Annually',
            'Every 6-12 months': 'Annually',
            'Annually': 'Every 1-2 years'
        },
        'II': {
            # Use base frequency
        },
        'III': {
            'Annually': 'Every 6 months',
            'Every 1-2 years': 'Annually',
            'Every 6-12 months': 'Every 6 months'
        },
        'IV': {
            'Annually': 'Every 3-6 months',
            'Every 1-2 years': 'Every 6 months',
            'Every 6-12 months': 'Every 3-6 months',
            'Every 6 months': 'Every 3 months'
        }
    }
    
    adjustments = frequency_adjustments.get(risk_class, {})
    return adjustments.get(base_frequency, base_frequency)


def has_family_history_for_disease(family_history: Dict, disease_id: str) -> bool:
    """Check if user has family history for this disease"""
    
    gen1 = family_history.get('generation_1', {})
    gen2 = family_history.get('generation_2', {})
    
    for relation, conditions in gen1.items():
        if isinstance(conditions, dict) and conditions.get(disease_id, False):
            return True
    
    for relation, conditions in gen2.items():
        if isinstance(conditions, dict) and conditions.get(disease_id, False):
            return True
    
    return False


def get_test_preparation_tips(test_name: str) -> List[str]:
    """Get preparation tips for specific tests"""
    
    tips = {
        'fasting blood glucose': [
            'Fast for 8-12 hours before test',
            'Only water allowed during fasting',
            'Schedule for early morning',
            'Continue regular medications unless told otherwise'
        ],
        'lipid profile': [
            'Fast for 9-12 hours before test',
            'Avoid alcohol 24 hours prior',
            'Maintain usual diet 2 weeks before',
            'Avoid heavy exercise night before'
        ],
        'hba1c': [
            'No fasting required',
            'Can be done any time of day',
            'Recent illness may affect results'
        ],
        'mammogram': [
            'Schedule week after period if premenopausal',
            'Avoid deodorant/powder on test day',
            'Wear two-piece outfit',
            'Bring previous mammogram images if available'
        ],
        'genetic testing': [
            'Genetic counseling recommended before testing',
            'Understand implications for family members',
            'Check insurance coverage',
            'No special preparation needed for blood draw'
        ]
    }
    
    test_lower = test_name.lower()
    
    for key, tip_list in tips.items():
        if key in test_lower:
            return tip_list
    
    return ['Follow standard pre-test instructions from your lab']


def get_test_cost_estimate(test_name: str, region: str = 'india') -> Dict[str, Any]:
    """
    Provide approximate cost estimates
    Note: These are rough estimates for demo purposes
    """
    
    # Rough estimates for India (INR)
    india_costs = {
        'hba1c': {'min': 300, 'max': 800, 'currency': 'INR'},
        'fasting blood glucose': {'min': 100, 'max': 300, 'currency': 'INR'},
        'lipid profile': {'min': 400, 'max': 1200, 'currency': 'INR'},
        'complete blood count': {'min': 200, 'max': 500, 'currency': 'INR'},
        'tsh': {'min': 300, 'max': 700, 'currency': 'INR'},
        'mammogram': {'min': 1500, 'max': 4000, 'currency': 'INR'},
        'genetic testing': {'min': 5000, 'max': 50000, 'currency': 'INR'},
        'ecg': {'min': 150, 'max': 500, 'currency': 'INR'},
        'stress test': {'min': 2000, 'max': 5000, 'currency': 'INR'}
    }
    
    test_lower = test_name.lower()
    
    for key, cost_info in india_costs.items():
        if key in test_lower:
            return {
                'estimated_cost': f"₹{cost_info['min']}-{cost_info['max']}",
                'note': 'Approximate cost - varies by lab and location'
            }
    
    return {
        'estimated_cost': 'Contact local lab',
        'note': 'Cost varies significantly by location and facility'
    }