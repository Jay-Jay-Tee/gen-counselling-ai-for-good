"""
Doctor consultation urgency logic
Determines when and why user should consult a healthcare provider
"""

from typing import Dict, Any, List


def get_consult_urgency(
    disease_id: str,
    risk_class: str,
    probability: float,
    user_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Determine consultation urgency and guidance
    
    Args:
        disease_id: Disease identifier
        risk_class: 'I', 'II', 'III', or 'IV'
        probability: Risk probability (0-1)
        user_data: User profile data
    
    Returns:
        Dictionary with urgency level, timeframe, and guidance
    """
    
    # Base urgency from risk class and probability
    urgency_level = determine_urgency_level(risk_class, probability)
    
    # Check for red flag conditions that escalate urgency
    urgency_level = check_red_flags(disease_id, user_data, urgency_level)
    
    # Get urgency details
    urgency_info = get_urgency_info(urgency_level)
    
    # Add disease-specific consultation guidance
    specialist_info = get_specialist_recommendation(disease_id, risk_class)
    
    return {
        'level': urgency_level,
        'timeframe': urgency_info['timeframe'],
        'message': urgency_info['message'],
        'specialist': specialist_info,
        'what_to_discuss': get_discussion_points(disease_id, risk_class),
        'preparation': get_consultation_preparation(disease_id)
    }


def determine_urgency_level(risk_class: str, probability: float) -> str:
    """
    Determine base urgency level
    Returns: 'none', 'routine', 'soon', 'urgent'
    """
    
    if risk_class == 'IV' or probability >= 0.80:
        return 'urgent'
    elif risk_class == 'III' or probability >= 0.60:
        return 'soon'
    elif risk_class == 'II' or probability >= 0.35:
        return 'routine'
    else:
        return 'none'


def check_red_flags(disease_id: str, user_data: Dict, current_urgency: str) -> str:
    """
    Check for red flag conditions that warrant escalating urgency
    """
    
    lab_values = user_data.get('lab_values', {})
    lifestyle = user_data.get('lifestyle', {})
    basic_info = user_data.get('basic_info', {})
    family = user_data.get('family', [])  # ✅ FIXED: use 'family' key
    
    # Helper to safely get numeric values
    def safe_get(d, key, default=0):
        val = d.get(key)
        return val if val is not None else default
    
    # Critical lab values
    if disease_id == 'type2_diabetes':
        hba1c = safe_get(lab_values, 'hba1c')
        fasting_glucose = safe_get(lab_values, 'fasting_glucose')
        
        if hba1c >= 7.0 or fasting_glucose >= 140:
            return 'urgent'
    
    elif disease_id == 'cad':
        ldl = safe_get(lab_values, 'ldl')
        systolic = safe_get(lab_values, 'systolic_bp')
        
        if ldl >= 190 or systolic >= 160:
            return 'urgent'
        
        # Smoking + high cholesterol + family history = urgent
        if lifestyle.get('smoking') and ldl >= 150:
            # Check for family history of CAD - ✅ FIXED: check known_issues array
            for member in family:
                known_issues = member.get('known_issues', [])
                if 'cad' in known_issues:
                    return 'urgent'
    
    elif disease_id == 'hypertension':
        systolic = safe_get(lab_values, 'systolic_bp')
        diastolic = safe_get(lab_values, 'diastolic_bp')
        
        if systolic >= 160 or diastolic >= 100:
            return 'urgent'
    
    elif disease_id == 'breast_ovarian_cancer':
        # Multiple first-degree relatives = urgent genetic counseling
        # First degree: parents (gen 1), siblings (gen 0), children (gen -1)
        # ✅ FIXED: check known_issues array
        first_degree_count = sum(
            1 for member in family
            if member.get('generation') in [-1, 0, 1]
            and 'breast_ovarian_cancer' in member.get('known_issues', [])
        )
        
        gen2_count = sum(
            1 for member in family
            if member.get('generation') == 2
            and 'breast_ovarian_cancer' in member.get('known_issues', [])
        )
        
        # If 2+ first-degree relatives OR 1 first-degree + 2 second-degree
        if first_degree_count >= 2 or (first_degree_count >= 1 and gen2_count >= 2):
            return 'urgent'
    
    # Age-based escalation
    age = basic_info.get('age', 30)
    if age > 50 and current_urgency == 'routine':
        return 'soon'
    
    # BMI-based escalation for metabolic diseases
    if disease_id in ['type2_diabetes', 'hypertension', 'pcos']:
        bmi = basic_info.get('bmi', 22)
        if bmi >= 35 and current_urgency == 'routine':
            return 'soon'
    
    return current_urgency


def get_urgency_info(urgency_level: str) -> Dict[str, str]:
    """Get information for each urgency level"""
    
    urgency_details = {
        'none': {
            'timeframe': 'No immediate consultation needed',
            'message': 'Continue healthy habits and schedule routine annual checkup'
        },
        'routine': {
            'timeframe': 'Schedule within 3-6 months',
            'message': 'Book a routine checkup to discuss screening and prevention strategies'
        },
        'soon': {
            'timeframe': 'Schedule within 4-6 weeks',
            'message': 'Consult your doctor soon to assess risk and develop prevention plan'
        },
        'urgent': {
            'timeframe': 'Schedule within 1-2 weeks',
            'message': 'Urgent consultation recommended - significant risk factors detected that require medical attention'
        }
    }
    
    return urgency_details.get(urgency_level, urgency_details['routine'])


def get_specialist_recommendation(disease_id: str, risk_class: str) -> Dict[str, str]:
    """Recommend appropriate specialist"""
    
    specialists = {
        'type2_diabetes': {
            'primary': 'Endocrinologist or Diabetologist',
            'alternative': 'Primary Care Physician or General Practitioner',
            'when_specialist': 'III or IV'
        },
        'cad': {
            'primary': 'Cardiologist',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'II or higher'
        },
        'hypertension': {
            'primary': 'Cardiologist or Hypertension Specialist',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'III or IV'
        },
        'familial_hypercholesterolemia': {
            'primary': 'Lipid Specialist or Cardiologist',
            'alternative': 'Endocrinologist',
            'when_specialist': 'Any risk class'
        },
        'breast_ovarian_cancer': {
            'primary': 'Genetic Counselor + Oncologist',
            'alternative': 'OB/GYN',
            'when_specialist': 'II or higher'
        },
        'thalassemia': {
            'primary': 'Hematologist + Genetic Counselor',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'Any risk class'
        },
        'sickle_cell': {
            'primary': 'Hematologist + Genetic Counselor',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'Any risk class'
        },
        'asthma': {
            'primary': 'Pulmonologist or Allergist',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'III or IV'
        },
        'hypothyroidism': {
            'primary': 'Endocrinologist',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'III or IV'
        },
        'pcos': {
            'primary': 'Endocrinologist or OB/GYN',
            'alternative': 'Primary Care Physician',
            'when_specialist': 'II or higher'
        }
    }
    
    default = {
        'primary': 'Primary Care Physician',
        'alternative': 'Appropriate specialist based on symptoms',
        'when_specialist': 'As recommended'
    }
    
    spec_info = specialists.get(disease_id, default)
    
    # Determine which doctor to recommend
    if risk_class in ['III', 'IV'] or spec_info['when_specialist'] in ['Any risk class', 'II or higher']:
        recommended = spec_info['primary']
    else:
        recommended = spec_info['alternative']
    
    return {
        'recommended': recommended,
        'also_consider': spec_info['alternative'] if recommended != spec_info['alternative'] else None
    }


def get_discussion_points(disease_id: str, risk_class: str) -> List[str]:
    """What to discuss with the doctor"""
    
    general_points = [
        "Your family medical history",
        "Current lifestyle and habits",
        "Risk assessment results and what they mean",
        "Recommended screening tests and frequency",
        "Prevention strategies specific to your risk level"
    ]
    
    disease_specific = {
        'type2_diabetes': [
            "Blood sugar levels and HbA1c results",
            "Diet plan and carbohydrate management",
            "Exercise recommendations",
            "Blood sugar monitoring if needed"
        ],
        'cad': [
            "Cholesterol levels and lipid profile",
            "Blood pressure management",
            "Cardiac risk assessment",
            "Stress test or cardiac imaging if warranted"
        ],
        'hypertension': [
            "Blood pressure readings and patterns",
            "Sodium reduction strategies",
            "Medication if BP consistently elevated",
            "Home BP monitoring plan"
        ],
        'breast_ovarian_cancer': [
            "Family cancer history in detail",
            "BRCA genetic testing options and implications",
            "Screening schedule (mammogram, MRI, ultrasound)",
            "Risk-reducing options if BRCA positive"
        ],
        'familial_hypercholesterolemia': [
            "Cholesterol levels and genetic testing",
            "Need for statin therapy",
            "Family screening recommendations",
            "Intensive cholesterol management plan"
        ]
    }
    
    points = list(general_points)
    
    if disease_id in disease_specific:
        points.extend(disease_specific[disease_id][:3])
    
    if risk_class in ['III', 'IV']:
        points.insert(0, "Urgency of intervention given your risk level")
    
    return points[:7]


def get_consultation_preparation(disease_id: str) -> List[str]:
    """How to prepare for the consultation"""
    
    preparation = [
        "Gather all recent medical records and test results",
        "Create detailed family medical history (2 generations)",
        "List all current medications and supplements",
        "Note any symptoms or concerns you've experienced",
        "Prepare questions about prevention and screening"
    ]
    
    disease_additions = {
        'type2_diabetes': [
            "Log blood sugar readings if you have them",
            "Keep food diary for 3-5 days before visit"
        ],
        'hypertension': [
            "Bring home blood pressure log if monitoring",
            "Note any headaches, dizziness, or chest discomfort"
        ],
        'breast_ovarian_cancer': [
            "Document all cancer cases in family with ages and types",
            "List any breast changes or concerns",
            "Bring previous mammogram reports if available"
        ],
        'cad': [
            "Note any chest pain, shortness of breath, or fatigue",
            "List all cardiac issues in immediate family"
        ]
    }
    
    if disease_id in disease_additions:
        preparation.extend(disease_additions[disease_id])
    
    return preparation[:7]