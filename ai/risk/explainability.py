"""
Generate human-readable explanations for risk predictions
Creates 'reasons' array explaining why a disease has a particular risk level
"""

from typing import Dict, List, Any


def generate_reasons(
    disease: Dict,
    user_data: Dict,
    family_score: float,
    lifestyle_score: float,
    lab_score: float
) -> List[str]:
    """
    Generate explanation for why this disease has this risk level
    
    Args:
        disease: Disease configuration
        user_data: All user input data
        family_score: Calculated family history score
        lifestyle_score: Calculated lifestyle score
        lab_score: Calculated lab score
    
    Returns:
        List of reason strings (3-5 reasons typically)
    """
    
    reasons = []
    disease_id = disease['id']
    disease_name = disease['name']
    
    # Get consult urgency to prioritize critical lab reasons
    probability = (family_score * 0.40 + lifestyle_score * 0.35 + lab_score * 0.25)
    is_urgent = probability >= 0.75
    
    # Family history reasons - FIXED: use 'family' key
    family_reasons = get_family_reasons(disease_id, user_data.get('family', []))
    
    # Lifestyle reasons
    lifestyle_reasons = get_lifestyle_reasons(
        disease.get('lifestyle_factors', []),
        user_data.get('lifestyle', {}),
        user_data.get('basic_info', {})
    )
    
    # Lab/biomarker reasons
    lab_reasons = get_lab_reasons(
        disease.get('lab_markers', []),
        user_data.get('lab_values', {}),
        disease.get('thresholds', {})
    )
    
    # If urgent, prioritize lab reasons first
    if is_urgent and lab_reasons:
        reasons.extend(lab_reasons[:2])  # Top 2 lab reasons first
        if family_reasons:
            reasons.extend(family_reasons[:1])
        if lifestyle_reasons:
            reasons.extend(lifestyle_reasons[:1])
    else:
        # Normal priority: family, lifestyle, lab
        if family_reasons:
            reasons.extend(family_reasons[:2])
        if lifestyle_reasons:
            reasons.extend(lifestyle_reasons[:2])
        if lab_reasons:
            reasons.extend(lab_reasons[:2])
    
    # If no specific reasons found, provide general reason based on scores
    if not reasons:
        if family_score > 0.4:
            reasons.append("Family history indicates predisposition")
        if lifestyle_score > 0.5:
            reasons.append("Lifestyle factors increase risk")
        if lab_score > 0.5:
            reasons.append("Biomarkers show concerning patterns")
    
    # Add age factor if relevant
    age = user_data.get('basic_info', {}).get('age', 30)
    if disease_id in ['type2_diabetes', 'cad', 'hypertension'] and age > 50:
        reasons.append(f"Age ({age}) increases risk for this condition")
    
    return reasons[:5]  # Return max 5 reasons


def get_family_reasons(disease_id: str, family: List[Dict]) -> List[str]:
    """Extract family history reasons from array format - FIXED"""
    reasons = []
    
    if not family:
        return reasons
    
    affected_by_generation = {
        -1: [],  # Children
        0: [],   # Siblings
        1: [],   # Parents
        2: []    # Extended family
    }
    
    # Group affected members by generation - FIXED: check known_issues array
    for member in family:
        known_issues = member.get('known_issues', [])
        if disease_id in known_issues:  # ✅ CORRECT: check if disease_id in array
            role = member.get('role', 'unknown')
            generation = member.get('generation', 2)
            
            # Format role name nicely
            role_label = role.replace('_', ' ').title()
            
            if generation in affected_by_generation:
                affected_by_generation[generation].append(role_label)
    
    # Build reason strings prioritizing closer generations
    
    # Parents (Gen 1) - Highest priority
    if affected_by_generation[1]:
        if len(affected_by_generation[1]) == 1:
            reasons.append(f"{affected_by_generation[1][0]} has this condition")
        else:
            reasons.append(f"Both parents affected: {' and '.join(affected_by_generation[1])}")
    
    # Siblings (Gen 0)
    if affected_by_generation[0]:
        if len(affected_by_generation[0]) == 1:
            reasons.append(f"{affected_by_generation[0][0]} has this condition")
        else:
            reasons.append(f"{len(affected_by_generation[0])} siblings affected by this condition")
    
    # Children (Gen -1) - Important for hereditary conditions
    if affected_by_generation[-1]:
        if len(affected_by_generation[-1]) == 1:
            reasons.append(f"{affected_by_generation[-1][0]} has this condition")
        else:
            reasons.append(f"{len(affected_by_generation[-1])} children affected")
    
    # Extended family (Gen 2)
    if affected_by_generation[2]:
        if len(affected_by_generation[2]) == 1:
            reasons.append(f"{affected_by_generation[2][0]} has this condition")
        elif len(affected_by_generation[2]) == 2:
            reasons.append(f"{' and '.join(affected_by_generation[2])} have this condition")
        else:
            reasons.append(f"{len(affected_by_generation[2])} relatives in previous generation affected")
    
    return reasons


def get_lifestyle_reasons(lifestyle_factors: List[str], lifestyle: Dict, basic_info: Dict) -> List[str]:
    """Extract lifestyle-based reasons"""
    reasons = []
    
    bmi = basic_info.get('bmi', 22)
    diet = lifestyle.get('diet', 'balanced')
    
    for factor in lifestyle_factors:
        if factor == 'obesity' and bmi >= 30:
            reasons.append(f"BMI of {bmi:.1f} indicates obesity, increasing risk")
        
        elif factor == 'obesity' and bmi >= 25:
            reasons.append(f"BMI of {bmi:.1f} indicates overweight status")
        
        elif factor == 'sedentary':
            exercise = lifestyle.get('exercise', 'regular')
            if exercise in ['sedentary', 'none', 'rare']:
                reasons.append("Sedentary lifestyle with minimal physical activity")
        
        elif factor == 'smoking' and lifestyle.get('smoking', False):
            reasons.append("Current smoking significantly elevates risk")
        
        elif factor == 'alcohol':
            alcohol = lifestyle.get('alcohol', 'none')
            if alcohol in ['heavy', 'frequent', 'daily']:
                reasons.append("Heavy alcohol consumption")
        
        elif factor == 'high_sugar' and diet == 'high_sugar':
            reasons.append("High sugar intake and poor dietary habits")
        
        elif factor == 'high_fat_diet' and diet == 'high_fat_diet':
            reasons.append("High-fat diet with frequent fried foods")
        
        elif factor == 'high_salt' and diet == 'high_salt':
            reasons.append("High sodium intake from processed foods")
        
        elif factor == 'stress':
            stress = lifestyle.get('stress_level', 'low')
            if stress in ['high', 'severe']:
                reasons.append("Chronic high stress levels")
    
    # Sleep issues
    sleep_hours = lifestyle.get('sleep_hours', 7)
    if sleep_hours < 6:
        reasons.append(f"Insufficient sleep ({sleep_hours} hours nightly)")
    
    return reasons


def get_lab_reasons(lab_markers: List[str], lab_values: Dict, thresholds: Dict) -> List[str]:
    """Extract lab/biomarker-based reasons - use non-diagnostic language"""
    reasons = []
    
    # Normalize lab keys (handle OCR variations)
    normalized_labs = {}
    for k, v in lab_values.items():
        key_lower = k.lower().replace(' ', '_').replace('-', '_')
        normalized_labs[key_lower] = v
    
    for marker in lab_markers:
        # Check both exact and normalized keys
        value = None
        if marker in lab_values:
            value = lab_values[marker]
        elif marker in normalized_labs:
            value = normalized_labs[marker]
        
        if value is None:
            continue
        
        # HbA1c
        if marker == 'hba1c':
            diabetic = thresholds.get('hba1c_diabetic', 6.5)
            prediabetic = thresholds.get('hba1c_prediabetic', 5.7)
            
            if value >= diabetic:
                reasons.append(f"HbA1c elevated at {value}%, suggesting higher diabetes risk")
            elif value >= prediabetic:
                reasons.append(f"HbA1c at {value}% indicates prediabetic pattern")
        
        # Fasting glucose
        elif marker == 'fasting_glucose':
            diabetic = thresholds.get('fasting_glucose_diabetic', 126)
            prediabetic = thresholds.get('fasting_glucose_prediabetic', 100)
            
            if value >= diabetic:
                reasons.append(f"Fasting glucose {value} mg/dL indicates diabetic range")
            elif value >= prediabetic:
                reasons.append(f"Fasting glucose {value} mg/dL suggests prediabetic state")
        
        # LDL cholesterol
        elif marker == 'ldl':
            very_high = thresholds.get('ldl_very_high', 190)
            high = thresholds.get('ldl_high', 130)
            
            if value >= very_high:
                reasons.append(f"LDL cholesterol very high at {value} mg/dL")
            elif value >= high:
                reasons.append(f"LDL cholesterol elevated at {value} mg/dL")
        
        # HDL cholesterol
        elif marker == 'hdl':
            low = thresholds.get('hdl_low', 40)
            
            if value < low:
                reasons.append(f"HDL cholesterol low at {value} mg/dL, reducing protection")
        
        # Triglycerides
        elif marker == 'triglycerides':
            high = thresholds.get('triglycerides_high', 150)
            
            if value >= 200:
                reasons.append(f"Triglycerides very high at {value} mg/dL")
            elif value >= high:
                reasons.append(f"Triglycerides elevated at {value} mg/dL")
        
        # Blood pressure
        elif marker == 'systolic_bp':
            if value >= 140:
                reasons.append(f"Systolic blood pressure high at {value} mmHg")
            elif value >= 130:
                reasons.append(f"Systolic blood pressure elevated at {value} mmHg")
        
        elif marker == 'diastolic_bp':
            if value >= 90:
                reasons.append(f"Diastolic blood pressure high at {value} mmHg")
        
        # TSH
        elif marker == 'tsh':
            high = thresholds.get('tsh_high', 4.5)
            if value >= high:
                reasons.append(f"TSH elevated at {value} mIU/L, suggesting thyroid dysfunction")
        
        # Hemoglobin
        elif marker == 'hemoglobin':
            low = thresholds.get('hemoglobin_low', 12.0)
            if value < low:
                reasons.append(f"Hemoglobin low at {value} g/dL, indicating anemia pattern")
        
        # Total cholesterol
        elif marker == 'total_cholesterol':
            very_high = thresholds.get('total_cholesterol_very_high', 300)
            high = thresholds.get('total_cholesterol_high', 200)
            
            if value >= very_high:
                reasons.append(f"Total cholesterol very high at {value} mg/dL")
            elif value >= high:
                reasons.append(f"Total cholesterol elevated at {value} mg/dL")
    
    return reasons