"""
Scoring logic for family history, lifestyle, and lab values
Returns normalized scores (0.0 - 1.0) for each component
"""

from typing import Dict, Any


def calculate_family_score(disease: Dict, family_history: Dict) -> float:
    """
    Calculate family history risk score
    
    Args:
        disease: Disease configuration dict
        family_history: {generation_1: {...}, generation_2: {...}}
    
    Returns:
        Score between 0.0 and 1.0
    """
    if not family_history:
        return 0.1  
    
    disease_id = disease['id']
    score = 0.0
    
    
    gen1 = family_history.get('generation_1', {})
    gen1_count = 0
    
    for relation, conditions in gen1.items():
        if isinstance(conditions, dict) and conditions.get(disease_id, False):
            gen1_count += 1
    
    
    gen2 = family_history.get('generation_2', {})
    gen2_count = 0
    
    for relation, conditions in gen2.items():
        if isinstance(conditions, dict) and conditions.get(disease_id, False):
            gen2_count += 1
    
    
    
    
    
    score += min(gen1_count * 0.30, 0.60)
    score += min(gen2_count * 0.10, 0.30)
    
    
    family_weight = disease.get('family_weight', 0.30)
    
    
    if family_weight >= 0.45:  
        score = min(1.0, score * 1.4)
    
    
    return min(0.95, max(0.1, score + 0.05))


def calculate_lifestyle_score(disease: Dict, lifestyle: Dict, basic_info: Dict) -> float:
    """
    Calculate lifestyle risk score
    
    Args:
        disease: Disease configuration dict
        lifestyle: User lifestyle data
        basic_info: Age, BMI, etc.
    
    Returns:
        Score between 0.0 and 1.0
    """
    if not lifestyle:
        return 0.2  
    
    disease_factors = disease.get('lifestyle_factors', [])
    
    if not disease_factors:
        
        return 0.15
    
    score = 0.0
    max_possible = len(disease_factors)
    
    
    for factor in disease_factors:
        if factor == 'obesity':
            bmi = basic_info.get('bmi', 22)
            if bmi >= 30:
                score += 1.0
            elif bmi >= 25:
                score += 0.5
        
        elif factor == 'sedentary':
            exercise = lifestyle.get('exercise', 'regular')
            if exercise in ['sedentary', 'none', 'rare']:
                score += 1.0
            elif exercise == 'occasional':
                score += 0.5
        
        elif factor == 'smoking':
            if lifestyle.get('smoking', False):
                score += 1.0
        
        elif factor == 'alcohol':
            alcohol = lifestyle.get('alcohol', 'none')
            if alcohol in ['heavy', 'frequent', 'daily']:
                score += 1.0
            elif alcohol in ['moderate', 'occasional']:
                score += 0.4
        
        elif factor == 'high_sugar':
            diet = lifestyle.get('diet', 'balanced')
            if diet in ['high_sugar', 'poor', 'junk_food']:
                score += 1.0
        
        elif factor == 'high_fat_diet':
            diet = lifestyle.get('diet', 'balanced')
            if diet in ['high_fat', 'fried', 'fast_food']:
                score += 1.0
        
        elif factor == 'high_salt':
            diet = lifestyle.get('diet', 'balanced')
            if diet in ['high_salt', 'processed']:
                score += 1.0
        
        elif factor == 'stress':
            stress = lifestyle.get('stress_level', 'low')
            if stress in ['high', 'severe']:
                score += 1.0
            elif stress == 'moderate':
                score += 0.5
        
        elif factor == 'air_pollution':
            
            score += 0.3  
        
        elif factor == 'allergen_exposure':
            score += 0.3  
    
    
    if max_possible > 0:
        normalized = score / max_possible
    else:
        normalized = 0.2
    
    
    sleep_hours = lifestyle.get('sleep_hours', 7)
    if sleep_hours < 6:
        normalized += 0.08
    
    return min(0.90, max(0.1, normalized))


def calculate_lab_score(disease: Dict, lab_values: Dict, thresholds: Dict) -> float:
    """
    Calculate lab/biomarker risk score
    
    Args:
        disease: Disease configuration dict
        lab_values: User's lab results
        thresholds: Disease-specific thresholds
    
    Returns:
        Score between 0.0 and 1.0
    """
    if not lab_values or not thresholds:
        return 0.15  
    
    lab_markers = disease.get('lab_markers', [])
    
    if not lab_markers:
        
        return 0.1
    
    score = 0.0
    markers_checked = 0
    
    for marker in lab_markers:
        if marker not in lab_values:
            continue
        
        value = lab_values[marker]
        markers_checked += 1
        
        
        if marker == 'hba1c':
            diabetic_threshold = thresholds.get('hba1c_diabetic', 6.5)
            prediabetic_threshold = thresholds.get('hba1c_prediabetic', 5.7)
            
            if value >= diabetic_threshold:
                score += 1.0
            elif value >= prediabetic_threshold:
                score += 0.6
        
        
        elif marker == 'fasting_glucose':
            diabetic_threshold = thresholds.get('fasting_glucose_diabetic', 126)
            prediabetic_threshold = thresholds.get('fasting_glucose_prediabetic', 100)
            
            if value >= diabetic_threshold:
                score += 1.0
            elif value >= prediabetic_threshold:
                score += 0.6
        
        
        elif marker == 'ldl':
            very_high = thresholds.get('ldl_very_high', 190)
            high = thresholds.get('ldl_high', 130)
            
            if value >= very_high:
                score += 1.0
            elif value >= high:
                score += 0.7
        
        
        elif marker == 'hdl':
            low_threshold = thresholds.get('hdl_low', 40)
            
            if value < low_threshold:
                score += 0.8
            elif value < 50:
                score += 0.4
        
        
        elif marker == 'triglycerides':
            high = thresholds.get('triglycerides_high', 150)
            
            if value >= 200:
                score += 1.0
            elif value >= high:
                score += 0.6
        
        
        elif marker == 'systolic_bp':
            elevated = thresholds.get('systolic_elevated', 130)
            
            if value >= 140:
                score += 1.0
            elif value >= elevated:
                score += 0.6
        
        elif marker == 'diastolic_bp':
            elevated = thresholds.get('diastolic_elevated', 80)
            
            if value >= 90:
                score += 1.0
            elif value >= elevated:
                score += 0.6
        
        
        elif marker == 'tsh':
            high = thresholds.get('tsh_high', 4.5)
            
            if value >= high:
                score += 0.8
        
        
        elif marker == 'hemoglobin':
            low = thresholds.get('hemoglobin_low', 12.0)
            
            if value < low:
                score += 0.7
        
        
        else:
            
            high_key = f"{marker}_high"
            low_key = f"{marker}_low"
            
            if high_key in thresholds and value >= thresholds[high_key]:
                score += 0.6
            elif low_key in thresholds and value <= thresholds[low_key]:
                score += 0.6
    
    
    if markers_checked > 0:
        normalized = score / markers_checked
    else:
        normalized = 0.15  
    
    return min(0.95, max(0.1, normalized))