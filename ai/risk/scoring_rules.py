"""
Scoring logic for family history, lifestyle, and lab values
Returns normalized scores (0.0 - 1.0) for each component
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def normalize_lab_key(key: str) -> str:
    """Normalize lab keys to handle variations from OCR"""
    key_lower = key.lower().replace(' ', '_').replace('-', '_')
    
    # Common variations mapping
    mappings = {
        'hba1c': ['hba1c', 'hemoglobin_a1c', 'glycated_hemoglobin'],
        'fasting_glucose': ['fasting_glucose', 'fasting_blood_sugar', 'fbs'],
        'ldl': ['ldl', 'ldl_cholesterol', 'low_density_lipoprotein'],
        'hdl': ['hdl', 'hdl_cholesterol', 'high_density_lipoprotein'],
        'triglycerides': ['triglycerides', 'tg'],
        'total_cholesterol': ['total_cholesterol', 'cholesterol'],
        'systolic_bp': ['systolic_bp', 'systolic', 'sbp'],
        'diastolic_bp': ['diastolic_bp', 'diastolic', 'dbp'],
        'tsh': ['tsh', 'thyroid_stimulating_hormone'],
        'hemoglobin': ['hemoglobin', 'hgb', 'hb']
    }
    
    for canonical, variants in mappings.items():
        if key_lower in variants:
            return canonical
    
    return key_lower


def calculate_family_score(disease: Dict, family: List[Dict]) -> float:
    """
    Calculate family history risk score
    
    Args:
        disease: Disease configuration dict
        family: List of family members with format:
            [
                {
                    "role": "mother",
                    "generation": 1,
                    "age": 58,
                    "known_issues": ["type2_diabetes", "hypertension"]
                }
            ]
    
    Returns:
        Score between 0.0 and 1.0
    """
    if not family:
        return 0.1  # Baseline
    
    disease_id = disease['id']
    score = 0.0
    
    # Count affected relatives by generation
    gen_minus1_count = 0  # Children
    gen0_count = 0        # Siblings
    gen1_count = 0        # Parents
    gen2_count = 0        # Grandparents/Aunts/Uncles
    
    for member in family:
        # Check if this member has the disease in their known_issues array
        known_issues = member.get('known_issues', [])
        if disease_id in known_issues:
            generation = member.get('generation', 2)
            
            if generation == -1:
                gen_minus1_count += 1
            elif generation == 0:
                gen0_count += 1
            elif generation == 1:
                gen1_count += 1
            else:  # generation == 2
                gen2_count += 1
    
    # Scoring logic
    # Gen -1 (Children): each affected = +0.25, max 0.50
    # Gen 0 (Siblings): each affected = +0.25, max 0.50
    # Gen 1 (Parents): each affected = +0.30, max 0.60
    # Gen 2 (Extended): each affected = +0.10, max 0.30
    
    score += min(gen_minus1_count * 0.25, 0.50)
    score += min(gen0_count * 0.25, 0.50)
    score += min(gen1_count * 0.30, 0.60)
    score += min(gen2_count * 0.10, 0.30)
    
    # Apply disease-specific family weight multiplier
    family_weight = disease.get('family_weight', 0.30)
    
    # For highly heritable diseases, amplify score
    if family_weight >= 0.45:  # BRCA, FH, Thalassemia, Sickle Cell
        score = min(1.0, score * 1.4)
    
    # Cap and add baseline
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
        return 0.2  # Baseline assuming average
    
    disease_factors = disease.get('lifestyle_factors', [])
    
    if not disease_factors:
        # No lifestyle factors for this disease (pure genetic)
        return 0.15
    
    score = 0.0
    max_possible = len(disease_factors)
    
    # Normalize diet value from lifestyle
    diet = lifestyle.get('diet', 'balanced')
    
    # Check each relevant lifestyle factor
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
            # Match with diseases_config.json lifestyle_factors
            if diet == 'high_sugar':
                score += 1.0
        
        elif factor == 'high_fat_diet':
            # Match with diseases_config.json lifestyle_factors
            if diet == 'high_fat_diet':
                score += 1.0
        
        elif factor == 'high_salt':
            # Match with diseases_config.json lifestyle_factors
            if diet == 'high_salt':
                score += 1.0
        
        elif factor == 'stress':
            stress = lifestyle.get('stress_level', 'low')
            if stress in ['high', 'severe']:
                score += 1.0
            elif stress == 'moderate':
                score += 0.5
        
        elif factor == 'air_pollution':
            # Assume urban = pollution
            score += 0.3  # Default moderate risk
        
        elif factor == 'allergen_exposure':
            score += 0.3  # Default moderate risk
        
        elif factor == 'iodine_deficiency':
            # Would need specific input - assume low baseline
            score += 0.2
        
        elif factor == 'hormone_therapy':
            # Would need specific input
            score += 0.2
    
    # Normalize
    if max_possible > 0:
        normalized = score / max_possible
    else:
        normalized = 0.2
    
    # Sleep factor (universal)
    sleep_hours = lifestyle.get('sleep_hours', 7)
    if sleep_hours < 6:
        normalized += 0.08
    
    return min(0.90, max(0.1, normalized))


def calculate_lab_score(disease: Dict, lab_values: Dict, thresholds: Dict) -> float:
    """
    Calculate lab/biomarker risk score
    
    Args:
        disease: Disease configuration dict
        lab_values: User's lab results (keys will be normalized)
        thresholds: Disease-specific thresholds
    
    Returns:
        Score between 0.0 and 1.0
    """
    if not lab_values or not thresholds:
        return 0.15  # No lab data = slight uncertainty
    
    # Normalize all lab keys
    normalized_labs = {normalize_lab_key(k): v for k, v in lab_values.items()}
    
    lab_markers = disease.get('lab_markers', [])
    
    if not lab_markers:
        # No lab markers for this disease
        return 0.1
    
    score = 0.0
    markers_checked = 0
    
    for marker in lab_markers:
        if marker not in normalized_labs:
            continue
        
        value = normalized_labs[marker]
        # Guard: skip None or non-numeric values (OCR may return strings)
        raw_value = value
        try:
            if value is None:
                logger.debug("Lab marker '%s' missing or None - skipping", marker)
                continue
            value = float(value)
        except (TypeError, ValueError):
            logger.debug("Non-numeric lab value for '%s': %r - skipping", marker, raw_value)
            continue
        markers_checked += 1
        
        # HbA1c scoring
        if marker == 'hba1c':
            diabetic_threshold = thresholds.get('hba1c_diabetic', 6.5)
            prediabetic_threshold = thresholds.get('hba1c_prediabetic', 5.7)
            
            if value >= diabetic_threshold:
                score += 1.0
            elif value >= prediabetic_threshold:
                score += 0.6
        
        # Fasting glucose
        elif marker == 'fasting_glucose':
            diabetic_threshold = thresholds.get('fasting_glucose_diabetic', 126)
            prediabetic_threshold = thresholds.get('fasting_glucose_prediabetic', 100)
            
            if value >= diabetic_threshold:
                score += 1.0
            elif value >= prediabetic_threshold:
                score += 0.6
        
        # LDL cholesterol
        elif marker == 'ldl':
            very_high = thresholds.get('ldl_very_high', 190)
            high = thresholds.get('ldl_high', 130)
            
            if value >= very_high:
                score += 1.0
            elif value >= high:
                score += 0.7
        
        # HDL cholesterol (lower is worse)
        elif marker == 'hdl':
            low_threshold = thresholds.get('hdl_low', 40)
            
            if value < low_threshold:
                score += 0.8
            elif value < 50:
                score += 0.4
        
        # Triglycerides
        elif marker == 'triglycerides':
            high = thresholds.get('triglycerides_high', 150)
            
            if value >= 200:
                score += 1.0
            elif value >= high:
                score += 0.6
        
        # Blood pressure
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
        
        # TSH (thyroid)
        elif marker == 'tsh':
            high = thresholds.get('tsh_high', 4.5)
            
            if value >= high:
                score += 0.8
        
        # Hemoglobin (low indicates anemia)
        elif marker == 'hemoglobin':
            low = thresholds.get('hemoglobin_low', 12.0)
            
            if value < low:
                score += 0.7
        
        # Generic threshold check for other markers
        else:
            # Check if marker has a threshold
            high_key = f"{marker}_high"
            low_key = f"{marker}_low"
            
            if high_key in thresholds and value >= thresholds[high_key]:
                score += 0.6
            elif low_key in thresholds and value <= thresholds[low_key]:
                score += 0.6
    
    # Normalize by number of markers checked
    if markers_checked > 0:
        normalized = score / markers_checked
    else:
        normalized = 0.15  # No relevant labs available
    
    return min(0.95, max(0.1, normalized))