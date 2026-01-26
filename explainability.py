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
    
    
    family_reasons = get_family_reasons(disease_id, user_data.get('family_history', {}))
    if family_reasons:
        reasons.extend(family_reasons[:2])  
    
    
    lifestyle_reasons = get_lifestyle_reasons(
        disease.get('lifestyle_factors', []),
        user_data.get('lifestyle', {}),
        user_data.get('basic_info', {})
    )
    if lifestyle_reasons:
        reasons.extend(lifestyle_reasons[:2])  
    
    
    lab_reasons = get_lab_reasons(
        disease.get('lab_markers', []),
        user_data.get('lab_values', {}),
        disease.get('thresholds', {})
    )
    if lab_reasons:
        reasons.extend(lab_reasons[:2])  
    
    
    if not reasons:
        if family_score > 0.4:
            reasons.append("Family history indicates genetic predisposition")
        if lifestyle_score > 0.5:
            reasons.append("Lifestyle factors increase risk")
        if lab_score > 0.5:
            reasons.append("Biomarkers show concerning patterns")
    
    
    age = user_data.get('basic_info', {}).get('age', 30)
    if disease_id in ['type2_diabetes', 'cad', 'hypertension'] and age > 50:
        reasons.append(f"Age ({age}) increases risk for this condition")
    
    return reasons[:5]  


def get_family_reasons(disease_id: str, family_history: Dict) -> List[str]:
    """Extract family history reasons"""
    reasons = []
    
    gen1 = family_history.get('generation_1', {})
    gen2 = family_history.get('generation_2', {})
    
    affected_gen1 = []
    affected_gen2 = []
    
    
    for relation, conditions in gen1.items():
        if isinstance(conditions, dict) and conditions.get(disease_id, False):
            affected_gen1.append(relation.replace('_', ' ').title())
    
    
    for relation, conditions in gen2.items():
        if isinstance(conditions, dict) and conditions.get(disease_id, False):
            affected_gen2.append(relation.replace('_', ' ').title())
    
    
    if affected_gen1:
        if len(affected_gen1) == 1:
            reasons.append(f"{affected_gen1[0]} has this condition")
        else:
            reasons.append(f"Multiple immediate family members affected ({', '.join(affected_gen1)})")
    
    if affected_gen2:
        if len(affected_gen2) == 1:
            reasons.append(f"{affected_gen2[0]} has this condition")
        elif len(affected_gen2) >= 2:
            reasons.append(f"Multiple relatives in previous generation affected")
    
    return reasons


def get_lifestyle_reasons(lifestyle_factors: List[str], lifestyle: Dict, basic_info: Dict) -> List[str]:
    """Extract lifestyle-based reasons"""
    reasons = []
    
    bmi = basic_info.get('bmi', 22)
    
    for factor in lifestyle_factors:
        if factor == 'obesity' and bmi >= 30:
            reasons.append(f"BMI of {bmi:.1f} indicates obesity")
        
        elif factor == 'obesity' and bmi >= 25:
            reasons.append(f"BMI of {bmi:.1f} indicates overweight")
        
        elif factor == 'sedentary':
            exercise = lifestyle.get('exercise', 'regular')
            if exercise in ['sedentary', 'none', 'rare']:
                reasons.append("Sedentary lifestyle with minimal physical activity")
        
        elif factor == 'smoking' and lifestyle.get('smoking', False):
            reasons.append("Current smoker")
        
        elif factor == 'alcohol':
            alcohol = lifestyle.get('alcohol', 'none')
            if alcohol in ['heavy', 'frequent', 'daily']:
                reasons.append("Heavy alcohol consumption")
        
        elif factor == 'high_sugar':
            diet = lifestyle.get('diet', 'balanced')
            if diet in ['high_sugar', 'poor', 'junk_food']:
                reasons.append("High sugar intake and poor dietary habits")
        
        elif factor == 'high_fat_diet':
            diet = lifestyle.get('diet', 'balanced')
            if diet in ['high_fat', 'fried', 'fast_food']:
                reasons.append("High-fat diet with frequent fried foods")
        
        elif factor == 'high_salt':
            diet = lifestyle.get('diet', 'balanced')
            if diet in ['high_salt', 'processed']:
                reasons.append("High sodium intake from processed foods")
        
        elif factor == 'stress':
            stress = lifestyle.get('stress_level', 'low')
            if stress in ['high', 'severe']:
                reasons.append("Chronic high stress levels")
    
    
    sleep_hours = lifestyle.get('sleep_hours', 7)
    if sleep_hours < 6:
        reasons.append(f"Insufficient sleep ({sleep_hours} hours nightly)")
    
    return reasons


def get_lab_reasons(lab_markers: List[str], lab_values: Dict, thresholds: Dict) -> List[str]:
    """Extract lab/biomarker-based reasons"""
    reasons = []
    
    for marker in lab_markers:
        if marker not in lab_values:
            continue
        
        value = lab_values[marker]
        
        
        if marker == 'hba1c':
            diabetic = thresholds.get('hba1c_diabetic', 6.5)
            prediabetic = thresholds.get('hba1c_prediabetic', 5.7)
            
            if value >= diabetic:
                reasons.append(f"HbA1c elevated at {value}% (diabetic range)")
            elif value >= prediabetic:
                reasons.append(f"HbA1c at {value}% indicates prediabetic state")
        
        
        elif marker == 'fasting_glucose':
            diabetic = thresholds.get('fasting_glucose_diabetic', 126)
            prediabetic = thresholds.get('fasting_glucose_prediabetic', 100)
            
            if value >= diabetic:
                reasons.append(f"Fasting glucose {value} mg/dL (diabetic range)")
            elif value >= prediabetic:
                reasons.append(f"Fasting glucose {value} mg/dL (prediabetic)")
        
        
        elif marker == 'ldl':
            very_high = thresholds.get('ldl_very_high', 190)
            high = thresholds.get('ldl_high', 130)
            
            if value >= very_high:
                reasons.append(f"LDL cholesterol very high at {value} mg/dL")
            elif value >= high:
                reasons.append(f"LDL cholesterol elevated at {value} mg/dL")
        
        
        elif marker == 'hdl':
            low = thresholds.get('hdl_low', 40)
            
            if value < low:
                reasons.append(f"HDL cholesterol low at {value} mg/dL")
        
        
        elif marker == 'triglycerides':
            high = thresholds.get('triglycerides_high', 150)
            
            if value >= 200:
                reasons.append(f"Triglycerides very high at {value} mg/dL")
            elif value >= high:
                reasons.append(f"Triglycerides elevated at {value} mg/dL")
        
        
        elif marker == 'systolic_bp':
            if value >= 140:
                reasons.append(f"Systolic blood pressure high at {value} mmHg")
            elif value >= 130:
                reasons.append(f"Systolic blood pressure elevated at {value} mmHg")
        
        elif marker == 'diastolic_bp':
            if value >= 90:
                reasons.append(f"Diastolic blood pressure high at {value} mmHg")
        
        
        elif marker == 'tsh':
            high = thresholds.get('tsh_high', 4.5)
            if value >= high:
                reasons.append(f"TSH elevated at {value} mIU/L")
        
        
        elif marker == 'hemoglobin':
            low = thresholds.get('hemoglobin_low', 12.0)
            if value < low:
                reasons.append(f"Hemoglobin low at {value} g/dL (anemia)")
        
        
        elif marker == 'total_cholesterol':
            very_high = thresholds.get('total_cholesterol_very_high', 300)
            high = thresholds.get('total_cholesterol_high', 200)
            
            if value >= very_high:
                reasons.append(f"Total cholesterol very high at {value} mg/dL")
            elif value >= high:
                reasons.append(f"Total cholesterol elevated at {value} mg/dL")
    
    return reasons